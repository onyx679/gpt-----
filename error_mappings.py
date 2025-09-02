"""
API错误信息映射配置
将技术性错误转换为用户友好的提示信息
"""

ERROR_MAPPINGS = {
    # RevenueCat API 错误映射
    'revenucat': {
        # 网络连接错误
        'OpenSSL SSL_connect: SSL_ERROR_SYSCALL in connection to api.revenuecat.com:443': '网络连接不稳定，请等几秒钟重试，不要换卡密。如仍失败请联系客服',
        'SSL_ERROR_SYSCALL': '网络连接异常，请检查网络后重试',
        'Connection timed out': 'RevenueCat服务连接超时，请稍后重试',
        'Couldn\'t connect to server': 'RevenueCat服务暂时不可用，请稍后重试',
        'Failed to connect': 'RevenueCat服务连接失败，请检查网络连接',
        'Connection refused': 'RevenueCat服务拒绝连接，请稍后重试',
        'Network is unreachable': '网络不可达，请检查网络设置',
        'SSL connect error': 'SSL连接错误，请稍后重试',
        'Operation timed out': 'RevenueCat服务响应超时，请稍后重试',
        
        # 收据相关错误
        'There is already another active subscriber using the same receipt': '此收据已被其他用户使用，请重新获取收据',
        'Invalid receipt': '收据格式无效，请重新获取收据数据',
        'Receipt validation failed': '收据验证失败，请检查收据数据是否正确',
        'Invalid receipt data': '收据数据无效，请确认收据完整性',
        'Receipt not found': '未找到有效收据，请重新获取',
        'Malformed receipt': '收据格式错误，请重新获取收据',
        
        # 服务器错误
        'Internal Server Error': 'RevenueCat服务内部错误，请稍后重试',
        'Service Unavailable': 'RevenueCat服务暂时不可用，请稍后重试',
        'Bad Gateway': 'RevenueCat服务网关错误，请稍后重试',
        'Gateway Timeout': 'RevenueCat服务网关超时，请稍后重试',
        
        # HTTP状态码错误
        '400': 'RevenueCat请求参数错误，请重新尝试',
        '401': 'RevenueCat认证失败，请稍后重试',
        '403': 'RevenueCat访问被拒绝，请稍后重试',
        '404': 'RevenueCat服务接口不存在，请联系技术支持',
        '429': 'RevenueCat请求过于频繁，请稍后重试',
        '500': 'RevenueCat服务内部错误，请稍后重试',
        '502': 'RevenueCat服务网关错误，请稍后重试',
        '503': 'RevenueCat服务暂时不可用，请稍后重试',
        '504': 'RevenueCat服务超时，请稍后重试',
    },
    
    # OpenAI API 错误映射
    'openai': {
        # Token认证错误
        '重新登录': 'Token已失效，请重新登录ChatGPT获取新Token重试，不要换卡密否则不提供售后。如仍失败请联系客服',

        # 账户权限错误
        'Request is not allowed. Please try again later': '该账户已绑定其他卡密，不能使用新卡密充值同一账户。可以重试原卡密，但换卡密充值不提供售后，如需帮助请联系客服',
        'No entitlements found for account': '该账户没有ChatGPT Plus订阅权限，请确认已购买订阅',
        'No entitlements found': '未找到有效的订阅权限，请确认账户状态',
        'Account not found': '账户不存在，请检查账户信息',
        'Invalid account': '账户信息无效，请重新登录',
        'Account suspended': '账户已被暂停，请联系OpenAI客服',
        'Account disabled': '账户已被禁用，请联系OpenAI客服',
        
        # Token相关错误
        'Invalid token': 'Token已过期或无效，请重新获取Token',
        'Token expired': 'Token已过期，请重新获取Token',
        'Authentication failed': '账户认证失败，请检查Token是否正确',
        'Unauthorized': '账户权限不足，请确认账户状态',
        'Invalid authorization': '授权信息无效，请重新获取Token',
        'Access denied': '访问被拒绝，请检查账户权限',
        
        # 网络连接错误
        'OpenSSL SSL_connect: SSL_ERROR_SYSCALL': '网络连接不稳定，请等几秒钟重试，不要换卡密。如仍失败请联系客服',
        'SSL_ERROR_SYSCALL': '网络连接异常，请检查网络后重试',
        'Connection timed out': 'OpenAI服务连接超时，请稍后重试',
        'Couldn\'t connect to server': 'OpenAI服务暂时不可用，请稍后重试',
        'Failed to connect': 'OpenAI服务连接失败，请检查网络连接',
        'Connection refused': 'OpenAI服务拒绝连接，请稍后重试',
        'Network is unreachable': '网络不可达，请检查网络设置',
        'SSL connect error': 'SSL连接错误，请稍后重试',
        'Operation timed out': 'OpenAI服务响应超时，请稍后重试',
        
        # 服务器错误
        'Internal Server Error': 'OpenAI服务内部错误，请稍后重试',
        'Service Unavailable': 'OpenAI服务暂时不可用，请稍后重试',
        'Bad Gateway': 'OpenAI服务网关错误，请稍后重试',
        'Gateway Timeout': 'OpenAI服务网关超时，请稍后重试',
        
        # HTTP状态码错误
        '0': '提示可能已经充值成功了，请刷新GPT网页，如未成功请更新token，如多次不行有问题请找客服',
        '400': 'OpenAI请求参数错误，请检查提交的数据',
        '401': 'OpenAI认证失败，请重新获取Token',
        '403': 'OpenAI访问被拒绝，请检查账户权限',
        '404': 'OpenAI服务接口不存在，请联系技术支持',
        '422': 'OpenAI数据验证失败，请检查账户信息',
        '429': 'OpenAI请求过于频繁，请稍后重试',
        '500': 'OpenAI服务内部错误，请稍后重试',
        '502': 'OpenAI服务网关错误，请稍后重试',
        '503': 'OpenAI服务暂时不可用，请稍后重试',
        '504': 'OpenAI服务超时，请稍后重试',
        
        # 业务逻辑错误
        'Subscription not active': '订阅未激活，请确认ChatGPT Plus订阅状态',
        'Payment required': '需要付费订阅，请购买ChatGPT Plus',
        'Quota exceeded': '使用配额已超限，请稍后重试',
        'Rate limit exceeded': '请求频率超限，请稍后重试',
    }
}


def get_friendly_error_message(error_message: str, service: str = 'openai') -> str:
    """
    根据错误信息获取用户友好的提示信息
    
    :param error_message: 原始错误信息
    :param service: 服务类型 (openai, revenuechat)
    :return: 用户友好的错误信息
    """
    if service not in ERROR_MAPPINGS:
        return error_message
    
    mappings = ERROR_MAPPINGS[service]
    
    # 精确匹配
    if error_message in mappings:
        return mappings[error_message]
    
    # 模糊匹配（包含关键词）
    for key, value in mappings.items():
        if key.lower() in error_message.lower():
            return value
    
    # 如果没有匹配到，返回原始错误信息
    return error_message


def map_http_status_error(status_code: int, service: str = 'openai') -> str:
    """
    根据HTTP状态码获取错误信息
    
    :param status_code: HTTP状态码
    :param service: 服务类型
    :return: 错误信息
    """
    if service not in ERROR_MAPPINGS:
        return f'HTTP错误: {status_code}'
    
    mappings = ERROR_MAPPINGS[service]
    status_str = str(status_code)
    
    if status_str in mappings:
        return mappings[status_str]
    
    # 默认错误信息
    if status_code >= 500:
        return f'服务器内部错误 ({status_code})，请稍后重试'
    elif status_code >= 400:
        return f'请求错误 ({status_code})，请检查输入信息'
    else:
        return f'HTTP错误: {status_code}'


