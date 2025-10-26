const API_BASE = "http://127.0.0.1:8000";
const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "index.html"; // اگر لاگین نیست، برگرد به login
}

async function fetchTodos() {
    const res = await fetch(`${API_BASE}/todos`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    const todos = await res.json();
    const todoList = document.getElementById("todoList");
    todoList.innerHTML = "";

    todos.forEach(todo => {
        const div = document.createElement("div");
        div.className = "bg-white p-4 shadow rounded flex justify-between items-center";
        div.innerHTML = `
            <div>
                <h3 class="font-bold">${todo.title}</h3>
                <p>${todo.description}</p>
            </div>
            <button onclick="deleteTodo(${todo.id})" class="bg-red-500 px-3 py-1 rounded text-white hover:bg-red-600">
                حذف
            </button>
        `;
        todoList.appendChild(div);
    });
}

fetchTodos();

const addBtn = document.getElementById("addTodoBtn");
addBtn.addEventListener("click", async () => {
    const title = document.getElementById("todoTitle").value;
    const desc = document.getElementById("todoDesc").value;

    await fetch(`${API_BASE}/todos`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title: title, description: desc })
    });

    document.getElementById("todoTitle").value = "";
    document.getElementById("todoDesc").value = "";
    fetchTodos();
});


async function deleteTodo(id) {
    await fetch(`${API_BASE}/todos/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    fetchTodos();
}


const logoutBtn = document.getElementById("logoutBtn");
logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("access_token");
    window.location.href = "index.html";
});
    
