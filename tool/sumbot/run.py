import os
import sys
import time
import signal
import psutil
import uvicorn
import argparse
import asyncio
import aiohttp
import json
from datetime import datetime

# 添加src目录到Python路径
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.append(SRC_DIR)

from src.utils.logger import get_logger
from src.utils.config_manager import ConfigManager

# 获取日志记录器
logger = get_logger("sumbot.service")

# PID文件路径
PID_FILE = os.path.join(ROOT_DIR, "sumbot.pid")

def get_pid():
    """获取服务进程ID"""
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        return pid
    except:
        return None

def save_pid(pid):
    """保存服务进程ID"""
    with open(PID_FILE, 'w') as f:
        f.write(str(pid))

def is_service_running():
    """检查服务是否运行中"""
    pid = get_pid()
    if pid:
        try:
            process = psutil.Process(pid)
            return process.is_running() and "python" in process.name().lower()
        except:
            return False
    return False

async def test_api_endpoints(host, port):
    """测试API端点"""
    base_url = f"http://{host}:{port}"
    test_results = []
    
    async with aiohttp.ClientSession() as session:
        # 测试根路径
        try:
            async with session.get(f"{base_url}/") as response:
                status = response.status
                test_results.append({
                    "endpoint": "/",
                    "method": "GET",
                    "status": status,
                    "success": status == 200
                })
        except Exception as e:
            test_results.append({
                "endpoint": "/",
                "method": "GET",
                "status": None,
                "error": str(e),
                "success": False
            })
        
        # 测试URL总结接口
        try:
            data = {"url": "https://example.com"}
            async with session.post(f"{base_url}/api/v1/summarize/url", json=data) as response:
                status = response.status
                test_results.append({
                    "endpoint": "/api/v1/summarize/url",
                    "method": "POST",
                    "status": status,
                    "success": status in [200, 400]  # 400是可接受的，因为example.com可能无法访问
                })
        except Exception as e:
            test_results.append({
                "endpoint": "/api/v1/summarize/url",
                "method": "POST",
                "status": None,
                "error": str(e),
                "success": False
            })
    
    return test_results

def stop_service():
    """停止服务"""
    pid = get_pid()
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            logger.info("正在停止服务...")
            # 等待进程结束
            for _ in range(10):
                if not is_service_running():
                    break
                time.sleep(0.5)
            else:
                # 如果进程仍在运行，强制结束
                try:
                    os.kill(pid, signal.SIGKILL)
                    logger.warning("服务未响应，强制终止")
                except:
                    pass
            logger.info("服务已停止")
        except ProcessLookupError:
            logger.warning("服务进程不存在")
        
        try:
            os.remove(PID_FILE)
        except:
            pass

def start_service(config):
    """启动服务"""
    if is_service_running():
        logger.warning("服务已在运行中")
        return
    
    # 保存当前进程ID
    save_pid(os.getpid())
    
    host = config.get('host', '0.0.0.0')
    port = config.get('port', 5566)
    
    logger.info(f"启动服务: http://{host}:{port}")
    logger.info(f"API文档: http://{host}:{port}/docs")
    
    # 启动服务
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=config.get('reload', True),
        reload_dirs=[SRC_DIR],
        log_config=None  # 使用我们自定义的日志配置
    )

def restart_service(config):
    """重启服务"""
    logger.info("开始重启服务...")
    stop_service()
    time.sleep(1)  # 等待服务完全停止
    start_service(config)

async def show_status():
    """显示服务状态"""
    if is_service_running():
        pid = get_pid()
        process = psutil.Process(pid)
        
        # 基本状态信息
        logger.info("服务状态")
        logger.info(f"进程ID: {pid}")
        logger.info(f"启动时间: {datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"CPU使用率: {process.cpu_percent()}%")
        logger.info(f"内存使用: {process.memory_info().rss / 1024 / 1024:.1f} MB")
        
        # 获取配置
        config = ConfigManager()
        api_config = config.get_api_config()
        host = api_config.get('host', '0.0.0.0')
        port = api_config.get('port', 5566)
        
        # 测试API端点
        logger.info("\n正在测试API端点...")
        test_results = await test_api_endpoints(host, port)
        
        # 显示测试结果
        logger.info("\nAPI测试结果:")
        for result in test_results:
            status = "成功" if result.get('success') else "失败"
            message = f"[{result['method']}] {result['endpoint']} - {status}"
            if 'error' in result:
                message += f" (错误: {result['error']})"
            logger.info(message)
    else:
        logger.warning("服务未运行")

def set_ai_service(service_name: str = None, api_key: str = None):
    """设置AI服务配置"""
    config_file = os.path.join(ROOT_DIR, "config.json")
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        ai_config = config_data.get('ai_service', {})
        
        # 更新默认服务
        if service_name:
            if service_name not in ai_config:
                raise ValueError(f"未知的服务名称: {service_name}")
            ai_config['default'] = service_name
            logger.info(f"已将默认服务设置为: {service_name}")
        
        # 更新API密钥
        if api_key:
            if not service_name:
                service_name = ai_config.get('default')
            if service_name in ai_config:
                if api_key.startswith('sk-'):
                    ai_config[service_name]['api_key'] = api_key
                    logger.info(f"已更新 {service_name} 的API密钥")
                else:
                    raise ValueError("API密钥必须以 'sk-' 开头")
        
        # 保存更新后的配置
        config_data['ai_service'] = ai_config
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        
        return True
    except Exception as e:
        logger.error(f"更新配置失败: {str(e)}")
        return False

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="SumBot服务管理")
    parser.add_argument('action', nargs='?', default='start',
                       choices=['start', 'stop', 'restart', 'status', 'set'],
                       help='执行的操作: start, stop, restart, status, set')
    parser.add_argument('--service', help='设置默认AI服务')
    parser.add_argument('--api-key', help='设置API密钥')
    args = parser.parse_args()
    
    # 加载配置
    config = ConfigManager()
    api_config = config.get_api_config()
    
    try:
        # 执行对应操作
        if args.action == 'set':
            if not (args.service or args.api_key):
                logger.error("请指定要设置的服务名称或API密钥")
            else:
                set_ai_service(args.service, args.api_key)
        elif args.action == 'start':
            start_service(api_config)
        elif args.action == 'stop':
            stop_service()
        elif args.action == 'restart':
            restart_service(api_config)
        elif args.action == 'status':
            asyncio.run(show_status())
    except KeyboardInterrupt:
        logger.warning("操作被用户中断")
    except Exception as e:
        logger.error(f"发生错误: {str(e)}") 