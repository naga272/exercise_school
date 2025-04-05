#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

from sqlalchemy         import create_engine, inspect, Column, Integer, String, Float, MetaData, Table, ForeignKey
from sqlalchemy.orm     import sessionmaker, declarative_base, relationship

import pythoncom
import threading
import platform
import time
import wmi
import sys
import os


debug = False

Base = declarative_base()


class AgentDB(Base):
    __tablename__ = "app_agentdb"
    id        = Column(Integer, primary_key=True, autoincrement=True)
    pcname    = Column(String(32), nullable=False)
    timestamp = Column(String(32), nullable=False)
    os        = Column(String(32), nullable=False)

    # Relazione con DiskDB (uno a molti)
    disks = relationship("DiskDB", backref="app_agentdb", cascade="all, delete-orphan")


class DiskDB(Base):
    __tablename__ = "app_diskdb"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    agent_id   = Column(Integer, ForeignKey('app_agentdb.id'), nullable=False)
    size_disk  = Column(String(32), nullable=False)
    disk_free  = Column(String(32), nullable=False)
    disk_name  = Column(String(32), nullable=False)


def task():
    engine = create_engine("sqlite:///./db.sqlite3")
    Session = sessionmaker(bind=engine)
    session = Session()

    pythoncom.CoInitialize() # a causa del thread, wmi mi da problemi se non metto questo col try-catch 
    try:
        wmi_istance = wmi.WMI()
        while True:
            disks = wmi.WMI().Win32_LogicalDisk()
            
            timestamp = time.time()
            pcname = platform.node()
            os_name = platform.system()

            agent_entry = AgentDB(
                pcname=pcname,
                timestamp=timestamp,
                os=os_name
            )
            session.add(agent_entry)
            session.commit()
            
            for disk in disks:
                disk_entry = DiskDB(
                    agent_id=agent_entry.id, 
                    size_disk=disk.Size, 
                    disk_free=disk.FreeSpace, 
                    disk_name=disk.Caption
                )
                
                session.add(disk_entry)
                session.commit()

            time.sleep(60 * 2)  
    finally:
        pythoncom.CoUninitialize()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CMDB.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    if debug == False and "runserver" in sys.argv:
        # avvia l'attivita' di scheduling solo quando voglio avviare il server
        scheduling = threading.Thread(target = task)
        scheduling.daemon = True
        scheduling.start()    
    
    main()
