# requests settings
DEFAULT_REQUEST_TIMEOUT = 10  # second
DEFAULT_MAX_REQUEST_RETRY = 3

# endpoints
SEND_MEMBER_SECRET_KEY_ENDPOINT = '/member/secret-key'
GEN_SESSION_ENDPOINT = '/otp/generate-session'
GET_SESSION_INFO_ENDPOINT = '/otp/session-data'
CONFIRM_SESSION_ENDPOINT = '/otp/session/confirm'
SEND_OTP_ENDPOINT = '/otp/send'
VERIFY_OTP_ENDPOINT = '/otp/verify'
