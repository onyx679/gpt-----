"""
ChongzhiPro API客户端类
用于调用 https://chongzhi.pro/ 的充值接口

使用示例：
client = ChongzhiProApiClient()
session = client.get_session()
result = client.verify_activation_code(session, 'CARD-XXXX-XXXX-XXXX')
if result['success']:
    reuse = client.reuse_record(session)
    recharge = client.submit_recharge(session, json_token)
"""

import requests
import json
import re
from typing import Dict, Optional, Any
from urllib.parse import urlparse


class ChongzhiProApiClient:
    def __init__(self, base_url: str = None):
        """
        构造函数
        :param base_url: 可选，自定义基础URL
        """
        self.base_url = base_url or 'https://chongzhi.pro'
        self.timeout = 30
        self.user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1'
        
        # 创建session对象以便复用连接
        self.session = requests.Session()
        self.session.verify = False  # 跳过SSL验证（对应PHP中的CURLOPT_SSL_VERIFYPEER => false）
        
    def get_session(self) -> Optional[str]:
        """
        获取Session ID
        访问主页获取 ios_gpt_session Cookie
        
        :return: Session ID 或 None（失败时）
        """
        url = f"{self.base_url}/"
        
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': self.user_agent,
            'Host': urlparse(self.base_url).netloc,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        }
        
        try:
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code != 200:
                return None
                
            # 提取 ios_gpt_session
            cookies = response.cookies
            if 'ios_gpt_session' in cookies:
                return cookies['ios_gpt_session']
                
            # 如果cookie中没有，尝试从Set-Cookie头中提取
            set_cookie_header = response.headers.get('Set-Cookie', '')
            match = re.search(r'ios_gpt_session=([^;]+)', set_cookie_header)
            if match:
                return match.group(1)
                
            return None
            
        except Exception as e:
            print(f"获取Session失败: {e}")
            return None
    
    def verify_activation_code(self, session: str, activation_code: str) -> Dict[str, Any]:
        """
        验证激活码
        
        :param session: Session ID
        :param activation_code: 激活码
        :return: 验证结果
        """
        url = f"{self.base_url}/api-verify.php"
        
        payload = {
            'activation_code': activation_code
        }
        
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'application/json',
            'Referer': f"{self.base_url}/",
            'Content-Type': 'application/json',
            'Origin': self.base_url,
            'Host': urlparse(self.base_url).netloc,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Cookie': f'ios_gpt_session={session}',
        }
        
        return self._send_request(url, 'POST', payload, headers)
    
    def reuse_record(self, session: str) -> Dict[str, Any]:
        """
        复用充值记录
        
        :param session: Session ID
        :return: 复用结果
        """
        url = f"{self.base_url}/api-recharge-reuse.php"
        
        payload = {
            'action': 'reuse_record'
        }
        
        headers = {
            'User-Agent': self.user_agent,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Content-Type': 'application/json',
            'Referer': f"{self.base_url}/",
            'Host': urlparse(self.base_url).netloc,
            'Accept': '*/*',
            'Origin': self.base_url,
            'Cookie': f'ios_gpt_session={session}',
        }
        
        return self._send_request(url, 'POST', payload, headers)
    
    def submit_recharge(self, session: str, user_data_json: str) -> Dict[str, Any]:
        """
        提交第一次充值
        
        :param session: Session ID
        :param user_data_json: 用户JSON Token数据
        :return: 充值结果
        """
        url = f"{self.base_url}/simple-submit-recharge.php"
        
        payload = {
            'user_data': user_data_json
        }
        
        headers = {
            'Origin': self.base_url,
            'User-Agent': self.user_agent,
            'Accept': 'application/json',
            'Host': urlparse(self.base_url).netloc,
            'Content-Type': 'application/json',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Referer': f"{self.base_url}/",
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': f'ios_gpt_session={session}',
        }
        
        return self._send_request(url, 'POST', payload, headers)
    
    def update_token_and_recharge(self, session: str, card_code: str, user_data_json: str) -> Dict[str, Any]:
        """
        更新Token并充值
        
        :param session: Session ID
        :param card_code: 卡密
        :param user_data_json: 用户JSON Token数据
        :return: 充值结果
        """
        url = f"{self.base_url}/api-recharge-reuse.php"
        
        payload = {
            'action': 'update_token_and_recharge',
            'card_code': card_code,
            'json_data': user_data_json
        }
        
        headers = {
            'User-Agent': self.user_agent,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Content-Type': 'application/json',
            'Referer': f"{self.base_url}/",
            'Host': urlparse(self.base_url).netloc,
            'Accept': '*/*',
            'Origin': self.base_url,
            'Cookie': f'ios_gpt_session={session}',
        }
        
        return self._send_request(url, 'POST', payload, headers)
    
    def _send_request(self, url: str, method: str = 'GET', data: Dict = None, headers: Dict = None) -> Dict[str, Any]:
        """
        发送HTTP请求
        
        :param url: 请求URL
        :param method: 请求方法
        :param data: 请求数据
        :param headers: 请求头
        :return: 响应结果
        """
        try:
            if method.upper() == 'POST':
                response = self.session.post(
                    url, 
                    json=data, 
                    headers=headers, 
                    timeout=self.timeout
                )
            else:
                response = self.session.get(
                    url, 
                    headers=headers, 
                    timeout=self.timeout
                )
            
            # 检查HTTP状态码
            if response.status_code not in [200, 201]:
                return {
                    'success': False,
                    'error': f'HTTP错误: {response.status_code}',
                    'http_code': response.status_code
                }
            
            # 尝试解析JSON响应
            try:
                result = response.json()
            except json.JSONDecodeError as e:
                return {
                    'success': False,
                    'error': f'JSON解析失败: {str(e)}',
                    'raw_response': response.text,
                    'http_code': response.status_code
                }
            
            # 添加HTTP状态码到结果中
            result['http_code'] = response.status_code
            return result
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': '请求超时',
                'http_code': 0
            }
        except requests.exceptions.ConnectionError as e:
            return {
                'success': False,
                'error': f'连接错误: {str(e)}',
                'http_code': 0
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'请求失败: {str(e)}',
                'http_code': 0
            }
    
    def full_recharge_process(self, activation_code: str, user_data_json: str = None) -> Dict[str, Any]:
        """
        完整的充值流程
        自动执行：获取Session -> 验证卡密 -> 复用/充值
        
        :param activation_code: 激活码
        :param user_data_json: 用户JSON Token（可选，用于第一次充值）
        :return: 完整流程结果
        """
        result = {
            'success': False,
            'steps': [],
            'final_result': None
        }
        
        # 步骤1：获取Session
        session = self.get_session()
        if not session:
            result['steps'].append({
                'step': 'get_session', 
                'success': False, 
                'error': '获取Session失败'
            })
            return result
        
        result['steps'].append({
            'step': 'get_session', 
            'success': True, 
            'session': session
        })
        
        # 步骤2：验证激活码
        verify_result = self.verify_activation_code(session, activation_code)
        result['steps'].append({
            'step': 'verify_code', 
            'success': verify_result.get('success', False), 
            'result': verify_result
        })
        
        if not verify_result.get('success', False):
            return result
        
        # 步骤3：根据卡密状态决定操作
        code_status = verify_result.get('data', {}).get('code_status', '')
        
        if code_status == 'used':
            # 已使用的卡密，尝试复用
            reuse_result = self.reuse_record(session)
            result['steps'].append({
                'step': 'reuse_record', 
                'success': reuse_result.get('success', False), 
                'result': reuse_result
            })
            result['final_result'] = reuse_result
            result['success'] = reuse_result.get('success', False)
        elif code_status == 'active' and user_data_json:
            # 未使用的卡密，进行第一次充值
            recharge_result = self.submit_recharge(session, user_data_json)
            result['steps'].append({
                'step': 'submit_recharge', 
                'success': recharge_result.get('success', False), 
                'result': recharge_result
            })
            result['final_result'] = recharge_result
            result['success'] = recharge_result.get('success', False)
        else:
            result['steps'].append({
                'step': 'decision', 
                'success': False, 
                'error': '卡密状态异常或缺少用户数据'
            })
        
        return result
    
    def set_timeout(self, timeout: int):
        """
        设置请求超时时间
        
        :param timeout: 超时时间（秒）
        """
        self.timeout = timeout
    
    def set_user_agent(self, user_agent: str):
        """
        设置User-Agent
        
        :param user_agent: User-Agent字符串
        """
        self.user_agent = user_agent
    
    def get_config(self) -> Dict[str, Any]:
        """
        获取当前配置信息
        
        :return: 配置信息
        """
        return {
            'base_url': self.base_url,
            'timeout': self.timeout,
            'user_agent': self.user_agent
        }


# 使用示例
if __name__ == "__main__":
    print("ChongzhiPro API客户端使用示例:\n")
    
    print("# 基础使用")
    print("client = ChongzhiProApiClient()")
    print("session = client.get_session()")
    print("if session:")
    print("    print(f'Session: {session}')")
    print("    ")
    print("    # 验证激活码")
    print("    result = client.verify_activation_code(session, 'CARD-XXXX-XXXX-XXXX')")
    print("    if result['success']:")
    print("        if result['data']['code_status'] == 'used':")
    print("            # 复用已有记录")
    print("            reuse = client.reuse_record(session)")
    print("            print(reuse)")
    print("        elif result['data']['code_status'] == 'active':")
    print("            # 第一次充值")
    print("            json_token = '{\"access_token\":\"...\",\"user\":{\"email\":\"...\"}}' # ChatGPT JSON数据")
    print("            recharge = client.submit_recharge(session, json_token)")
    print("            print(recharge)")
    print()
    
    print("# 完整流程（推荐）")
    print("client = ChongzhiProApiClient()")
    print("json_token = '{\"access_token\":\"...\",\"user\":{\"email\":\"...\"}}' # ChatGPT JSON数据")
    print("result = client.full_recharge_process('CARD-XXXX-XXXX-XXXX', json_token)")
    print("print(result)")


