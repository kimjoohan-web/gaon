# config/settings/summernote.py
# code by 하얀설표(https://django.seolpyo.com/)

SUMMERNOTE_CONFIG = { # django-summernote에 적용되는 설정
    'iframe': True,
    'summernote': {
        'width': '100%', # 기본 너비
        'height': '600', # 기본 높이
        'lang': 'ko-KR', # 기본 언어
    },
    'css': (
        '/static/style.css', # 사용자 정의 css 추가
    ),
}