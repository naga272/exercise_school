


def binary_search(arr, target):
    """
    Esegue una ricerca binaria per trovare `target` nella lista ordinata `arr`.
    Restituisce 1 se `target` è trovato, altrimenti 0.
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2  # Trova il punto medio

        if arr[mid] == target:
            return 1  # Trovato
        elif arr[mid] < target:
            left = mid + 1  # Cerca nella metà destra
        else:
            right = mid - 1  # Cerca nella metà sinistra

    return 0  # Non trovato