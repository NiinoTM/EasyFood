import os
import shutil
import logging
from datetime import datetime

class BackupManager:
    def __init__(self):
        self.backup_dir = "backups"
        os.makedirs(self.backup_dir, exist_ok=True)
        
        logging.basicConfig(
            filename='backup.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def create_backup(self):
        """Cria backup com timestamp único e evita duplicatas"""
        try:
            # 1. Gera timestamp com milissegundos
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Formato: AAAAMMDD_HHMMSS_MMM
            
            # 2. Verifica colisões e cria nome único
            backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}")
            counter = 1
            while os.path.exists(backup_path):
                backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}_{counter}")
                counter += 1
            
            # 3. Copia arquivos
            os.makedirs(backup_path)
            data_files = [
                'data/foods.json',
                'data/suppliers.json',
                'data/stock_entries.json',
                'data/stock_exits.json',
                'data/meals.json'
            ]
            
            for file in data_files:
                if os.path.exists(file):
                    shutil.copy2(file, backup_path)
            
            # 4. Rotação inteligente (mantém últimos 20 backups)
            self._rotate_backups()
            
            logging.info(f"Backup criado: {backup_path}")
            return True
            
        except Exception as e:
            logging.error(f"Falha no backup: {str(e)}")
            return False

    def _rotate_backups(self):
        """Remove backups antigos baseado na data de criação real"""
        backups = []
        for entry in os.listdir(self.backup_dir):
            if entry.startswith("backup_"):
                path = os.path.join(self.backup_dir, entry)
                stats = os.stat(path)
                backups.append((stats.st_ctime, path))  # Usa timestamp de criação
        
        # Ordena do mais novo para o mais antigo
        backups.sort(reverse=True, key=lambda x: x[0])
        
        # Mantém apenas os 20 mais recentes
        for entry in backups[20:]:
            try:
                shutil.rmtree(entry[1])
                logging.info(f"Backup removido: {entry[1]}")
            except Exception as e:
                logging.error(f"Falha ao remover backup {entry[1]}: {str(e)}")

    def list_backups(self):
        """Lista backups ordenados por data de criação"""
        backups = []
        for entry in os.listdir(self.backup_dir):
            if entry.startswith("backup_"):
                path = os.path.join(self.backup_dir, entry)
                ctime = datetime.fromtimestamp(os.stat(path).st_ctime)
                backups.append((ctime, entry))
        
        # Ordena do mais novo para o mais antigo
        backups.sort(reverse=True, key=lambda x: x[0])
        
        print("\n📂 Backups Disponíveis:")
        for idx, (ctime, entry) in enumerate(backups, 1):
            print(f"{idx}. {entry} - Criado em: {ctime.strftime('%d/%m/%Y %H:%M:%S')}")
        
        return [entry[1] for entry in backups]

    def restore_backup(self):  # <--- MÉTODO ADICIONADO
        """Restaura backup selecionado"""
        try:
            backups = sorted(
                [d for d in os.listdir(self.backup_dir) if d.startswith("backup_")],
                reverse=True
            )
            
            if not backups:
                print("Nenhum backup disponível!")
                return False
            
            print("\n📂 Backups Disponíveis:")
            for idx, backup in enumerate(backups, 1):
                print(f"{idx}. {backup[7:19]}")  # Exemplo: backup_20240715_1430 → 20240715_1430
                
            choice = input("\nDigite o número do backup: ")
            if not choice.isdigit():
                print("Entrada inválida!")
                return False
                
            idx = int(choice) - 1
            if 0 <= idx < len(backups):
                selected = backups[idx]
                source = os.path.join(self.backup_dir, selected)
                
                confirm = input(f"\n⚠️ RESTAURAR {selected}? ISSO SOBRESCREVERÁ DADOS ATUAIS! (s/n): ")
                if confirm.lower() != 's':
                    return False
                
                # Substitui arquivos
                for file in os.listdir(source):
                    shutil.copy(
                        os.path.join(source, file),
                        os.path.join("data", file)
                    )
                    
                print("✅ Restauração concluída! Reinicie o sistema.")
                return True
                
            print("Número inválido!")
            return False
            
        except Exception as e:
            logging.error(f"Erro na restauração: {str(e)}")
            print(f"❌ Falha crítica: {str(e)}")
            return False

# Instância global
backup_manager = BackupManager()