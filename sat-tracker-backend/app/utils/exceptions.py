from fastapi import HTTPException

class UpstreamAuthError(HTTPException):
    def __init__(self, detail="Invalid or missing N2YO API key"):
        super().__init__(status_code=401, detail=detail)

class UpstreamRateLimited(HTTPException):
    def __init__(self, detail="Upstream rate limit exceeded"):
        super().__init__(status_code=429, detail=detail)

class UpstreamError(HTTPException):
    def __init__(self, status_code=502, detail="N2YO upstream error"):
        super().__init__(status_code=status_code, detail=detail)
