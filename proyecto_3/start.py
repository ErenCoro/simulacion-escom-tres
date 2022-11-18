import uvicorn


if __name__ == "__main__":
	uvicorn.run('src.app.service:app' , host = '127.0.0.1', port = 8125, log_level = 'info')

	