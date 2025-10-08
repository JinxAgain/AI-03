# Todo Front (React)

React-based single-page UI for the Todo application in `todo-app/req.md`, integrating with the FastAPI backend via the API contract in `TECH_ARCHITECTURE.md`.

## Features
- 标题、输入框、添加按钮、序列表展示
- 添加待办、标记完成、删除
- 过滤：全部 / 未完成 / 已完成
- 清除已完成、清除全部
- 现代、简洁的 CSS，主体最大宽度 800px，hover 视觉反馈

## Run (local)
1. Start the backend first
   - See `todo-app/backend/README.md`
   - Default: http://127.0.0.1:8000
2. Open the frontend
   - Option A: Double-click `front/index.html` to open in your browser
   - Option B: Use a static server (e.g., VS Code Live Server) to serve `front/`

If your backend runs on a different URL, append `?api=YOUR_URL` when opening the page, for example:
```
file:///.../front/index.html?api=http://127.0.0.1:8000
```

## Notes
- The app uses React via CDN and Babel Standalone for quick development. No build step is required.
- CORS is enabled on the backend for local development.
- All API endpoints are described in `TECH_ARCHITECTURE.md`.
