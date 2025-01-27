
from src.modules.backup_manager import BackupManager
import sys

if __name__ == "__main__":
    bm = BackupManager()
    
    if len(sys.argv) == 2 and sys.argv[1] == "list":
        bm.list_backups()
    elif len(sys.argv) == 3 and sys.argv[1] == "restore":
        bm.restore_backup(int(sys.argv[2]))
    else:
        print("Uso:")
        print("  Listar backups: python restore.py list")
        print("  Restaurar: python restore.py restore <numero>")