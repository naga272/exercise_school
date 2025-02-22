from django.db import models

# Create your models here.


class AgentDB(models.Model):
    pcname = models.CharField(max_length=255)
    timestamp = models.FloatField(unique=True)
    os = models.CharField(max_length=255)

    def __str__(self):
        return f"pcname: {self.pcname}, timestamp: {self.timestamp} os: {self.os}"


class DiskDB(models.Model):
    agent = models.ForeignKey(AgentDB, on_delete=models.CASCADE, related_name="disks")
    disk_name = models.CharField(max_length=255)
    size_disk = models.BigIntegerField()
    disk_free = models.BigIntegerField()

    def __str__(self):
        return f"{self.disk_name} ({self.size_disk} bytes)"
