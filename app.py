"""
GPT充值系统 - Flask主应用
基于Python Flask框架的GPT充值系统
"""

from flask import Flask, render_template, request, jsonify, session
import re
import json
import os
from typing import Dict, Any
import logging
from datetime import datetime

from api_client import ChongzhiProApiClient
from error_mappings import get_friendly_error_message, map_http_status_error

# 创建Flask应用
app = Flask(__name__)

# 配置
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SESSION_TIMEOUT'] = int(os.environ.get('SESSION_TIMEOUT', '1800'))  # 30分钟

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gpt_recharge.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def validate_activation_code(code: str) -> bool:
    """验证激活码格式"""
    pattern = r'^CARD-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$'
    return bool(re.match(pattern, code, re.IGNORECASE))


def log_api_call(action: str, success: bool, data: Dict = None, error: str = None):
    """记录API调用日志"""
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'success': success,
        'client_ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', '')
    }
    
    if error:
        log_data['error'] = error
    if data:
        log_data['data'] = data
    
    if success:
        logger.info(f"API调用成功: {json.dumps(log_data, ensure_ascii=False)}")
    else:
        logger.error(f"API调用失败: {json.dumps(log_data, ensure_ascii=False)}")


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/verify-code', methods=['POST'])
def verify_code():
    """验证激活码API"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': '请求数据格式错误'})
        
        activation_code = data.get('activation_code', '').strip()
        
        if not activation_code:
            return jsonify({'success': False, 'error': '请输入激活码'})
        
        if not validate_activation_code(activation_code):
            return jsonify({'success': False, 'error': '激活码格式不正确'})
        
        # 创建API客户端
        client = ChongzhiProApiClient()
        
        # 获取会话
        session_id = client.get_session()
        if not session_id:
            log_api_call('verify_code', False, error='无法获取会话')
            return jsonify({'success': False, 'error': '无法获取会话，请稍后重试'})
        
        # 验证激活码
        verify_result = client.verify_activation_code(session_id, activation_code)
        
        if not verify_result.get('success', False):
            error_msg = get_friendly_error_message(
                verify_result.get('error', '验证失败'), 
                'openai'
            )
            log_api_call('verify_code', False, error=error_msg)
            return jsonify({'success': False, 'error': error_msg})
        
        # 保存会话信息
        session['cz_session'] = session_id
        session['cz_code'] = activation_code
        session['cz_verify'] = verify_result
        
        # 提取结果数据
        data_result = verify_result.get('data', {})
        status = data_result.get('code_status', '')
        email = data_result.get('existing_record', {}).get('bound_email_masked', '')
        has_existing = bool(data_result.get('existing_record'))
        
        result = {
            'success': True,
            'status': status,
            'is_new': not has_existing,
            'email': email
        }
        
        log_api_call('verify_code', True, {'status': status, 'is_new': not has_existing})
        return jsonify(result)
        
    except Exception as e:
        logger.exception("验证激活码时发生异常")
        return jsonify({'success': False, 'error': f'服务器错误：{str(e)}'})


@app.route('/api/submit-json', methods=['POST'])
def submit_json():
    """提交JSON Token API"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': '请求数据格式错误'})
        
        json_token = data.get('json_token', '').strip()
        
        if not json_token:
            return jsonify({'success': False, 'error': '请粘贴JSON Token'})
        
        if 'cz_session' not in session:
            return jsonify({'success': False, 'error': '会话失效，请重新验证激活码'})
        
        # 创建API客户端并提交充值
        client = ChongzhiProApiClient()
        result = client.submit_recharge(session['cz_session'], json_token)
        
        # 处理错误信息
        if not result.get('success', False):
            error_msg = get_friendly_error_message(
                result.get('error', '充值失败'), 
                'openai'
            )
            result['error'] = error_msg
        
        log_api_call('submit_json', result.get('success', False), 
                    error=result.get('error') if not result.get('success', False) else None)
        
        return jsonify(result)
        
    except Exception as e:
        logger.exception("提交JSON Token时发生异常")
        return jsonify({'success': False, 'error': f'服务器错误：{str(e)}'})


@app.route('/api/reuse-record', methods=['POST'])
def reuse_record():
    """复用充值记录API"""
    try:
        if 'cz_session' not in session:
            return jsonify({'success': False, 'error': '会话失效，请重新验证激活码'})
        
        # 创建API客户端并复用记录
        client = ChongzhiProApiClient()
        result = client.reuse_record(session['cz_session'])
        
        # 处理错误信息
        if not result.get('success', False):
            error_msg = get_friendly_error_message(
                result.get('error', '复用失败'), 
                'openai'
            )
            result['error'] = error_msg
        
        log_api_call('reuse_record', result.get('success', False),
                    error=result.get('error') if not result.get('success', False) else None)
        
        return jsonify(result)
        
    except Exception as e:
        logger.exception("复用充值记录时发生异常")
        return jsonify({'success': False, 'error': f'服务器错误：{str(e)}'})


@app.route('/api/update-token', methods=['POST'])
def update_token():
    """更新Token API"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': '请求数据格式错误'})
        
        json_token = data.get('json_token', '').strip()
        
        if not json_token:
            return jsonify({'success': False, 'error': '请粘贴JSON Token'})
        
        if 'cz_session' not in session or 'cz_code' not in session:
            return jsonify({'success': False, 'error': '会话失效，请重新验证激活码'})
        
        # 创建API客户端并更新Token
        client = ChongzhiProApiClient()
        result = client.update_token_and_recharge(
            session['cz_session'], 
            session['cz_code'], 
            json_token
        )
        
        # 处理错误信息
        if not result.get('success', False):
            error_msg = get_friendly_error_message(
                result.get('error', '更新失败'), 
                'openai'
            )
            result['error'] = error_msg
        
        log_api_call('update_token', result.get('success', False),
                    error=result.get('error') if not result.get('success', False) else None)
        
        return jsonify(result)
        
    except Exception as e:
        logger.exception("更新Token时发生异常")
        return jsonify({'success': False, 'error': f'服务器错误：{str(e)}'})


@app.route('/api/health')
def health_check():
    """健康检查API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@app.errorhandler(404)
def not_found_error(error):
    """404错误处理"""
    return render_template('error.html', 
                         error_code=404, 
                         error_message='页面未找到'), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    logger.exception("服务器内部错误")
    return render_template('error.html', 
                         error_code=500, 
                         error_message='服务器内部错误'), 500


@app.before_request
def before_request():
    """请求前处理"""
    # 记录请求日志
    if request.endpoint and request.endpoint.startswith('api'):
        logger.info(f"API请求: {request.method} {request.path} - IP: {request.remote_addr}")


if __name__ == '__main__':
    # 开发环境运行
    app.run(debug=True, host='0.0.0.0', port=5000)



