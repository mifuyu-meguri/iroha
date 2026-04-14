import urllib.request

def ifInternet(timeout:float=3) -> bool:
    try:
        with urllib.request.urlopen("http://www.msftconnecttest.com/connecttest.txt", timeout=timeout) as response:
            return (response.read().decode("utf-8", errors="ignore").strip() == "Microsoft Connect Test")
    except Exception:
        return False
