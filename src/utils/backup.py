import os
import shutil
import winreg
from datetime import datetime
from logger.initLogger import log

def backup_asar_and_aura(asar_path, aura_path):
    """
    备份ASAR文件、aura目录和注册表到临时目录
    :param asar_path: ASAR文件路径
    :param aura_path: aura目录路径
    :return: 备份目录路径
    """
    # 创建带时间戳的备份目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(os.getenv("TEMP"), "HugoAura-Install", timestamp)
    
    # 确保目录存在
    os.makedirs(backup_dir, exist_ok=True)
    log.info(f"开始备份到目录: {backup_dir}")
    
    try:
        # 备份ASAR文件
        if os.path.isfile(asar_path):
            shutil.copy2(asar_path, os.path.join(backup_dir, os.path.basename(asar_path)))
        
        # 备份aura目录
        if os.path.isdir(aura_path):
            shutil.copytree(aura_path, os.path.join(backup_dir, "aura"))
        
        # 备份注册表
        try:
            reg_file = os.path.join(backup_dir, "HugoAura.reg")
            with open(reg_file, 'w') as f:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\HugoAura")
                winreg.SaveKey(key, reg_file)
                winreg.CloseKey(key)
        except WindowsError as e:
            log.error(f"注册表备份失败: {e}")
        
        log.info("备份完成")
        return backup_dir
    except Exception as e:
        log.error(f"备份失败: {e}")
        return None