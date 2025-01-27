# src/modules/backup_manager.py
import os
import shutil
import logging
from datetime import datetime

class BackupManager:
    def __init__(self):
        self.backup_dir = "backups"  # Diretório onde os backups serão armazenados
        os.makedirs(self.backup_dir, exist_ok=True)  # Cria o diretório se não existir

        # Configuração do sistema de logs
        logging.basicConfig(
            filename='backup.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def create_backup(self):
        """
        Cria um backup dos arquivos de dados com um timestamp único.
        """
        try:
            # Gera um timestamp com milissegundos
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Formato: AAAAMMDD_HHMMSS_MMM

            # Verifica colisões e cria um nome único para o backup
            backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}")
            counter = 1
            while os.path.exists(backup_path):
                backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}_{counter}")
                counter += 1

            # Cria o diretório do backup
            os.makedirs(backup_path)

            # Lista dos arquivos de dados que serão copiados
            data_files = [
                'data/foods.json',
                'data/suppliers.json',
                'data/stock_entries.json',
                'data/stock_exits.json',
                'data/meals.json'
            ]

            # Copia os arquivos para o diretório de backup
            for file in data_files:
                if os.path.exists(file):
                    shutil.copy2(file, backup_path)

            # Realiza a rotação de backups (mantém apenas os últimos 20 backups)
            self._rotate_backups()

            logging.info(f"Backup criado: {backup_path}")
            return True

        except Exception as e:
            logging.error(f"Falha no backup: {str(e)}")
            return False

    def _rotate_backups(self):
        """
        Remove backups antigos, mantendo apenas os últimos 20 backups.
        """
        backups = []
        for entry in os.listdir(self.backup_dir):
            if entry.startswith("backup_"):
                path = os.path.join(self.backup_dir, entry)
                stats = os.stat(path)
                backups.append((stats.st_ctime, path))  # Usa o timestamp de criação

        # Ordena os backups do mais novo para o mais antigo
        backups.sort(reverse=True, key=lambda x: x[0])

        # Mantém apenas os 20 backups mais recentes
        for entry in backups[20:]:
            try:
                shutil.rmtree(entry[1])  # Remove o backup
                logging.info(f"Backup removido: {entry[1]}")
            except Exception as e:
                logging.error(f"Falha ao remover backup {entry[1]}: {str(e)}")

    def list_backups(self):
        """
        Lista todos os backups disponíveis, ordenados por data de criação.
        """
        backups = []
        for entry in os.listdir(self.backup_dir):
            if entry.startswith("backup_"):
                path = os.path.join(self.backup_dir, entry)
                ctime = datetime.fromtimestamp(os.stat(path).st_ctime)
                backups.append((ctime, entry))

        # Ordena os backups do mais novo para o mais antigo
        backups.sort(reverse=True, key=lambda x: x[0])

        # Retorna a lista de backups
        return [entry[1] for entry in backups]

    def restore_backup(self, backup_name):
        """
        Restaura um backup específico, sobrescrevendo os arquivos de dados atuais.
        """
        try:
            backup_path = os.path.join(self.backup_dir, backup_name)
            if not os.path.exists(backup_path):
                return False, "Backup não encontrado!"

            # Substitui os arquivos de dados atuais pelos do backup
            for file in os.listdir(backup_path):
                shutil.copy(
                    os.path.join(backup_path, file),
                    os.path.join("data", file)
                )

            logging.info(f"Backup restaurado: {backup_path}")
            return True, "Backup restaurado com sucesso!"

        except Exception as e:
            logging.error(f"Erro na restauração: {str(e)}")
            return False, f"Falha na restauração: {str(e)}"

# Instância global do BackupManager
backup_manager = BackupManager()