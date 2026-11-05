const BASE_URL = ""; // Укажите порт вашего FastAPI
let editingTaskId = null;

// Загрузка списка задач (GET)
async function loadTasks() {
  try {
    const response = await fetch(`${BASE_URL}/tasks`);
    const tasks = await response.json();
    const taskList = document.getElementById("taskList");
    taskList.innerHTML = "";

    if (tasks.length === 0) {
      taskList.innerHTML = "<li>Задач пока нет</li>";
      return;
    }

    tasks.forEach((task) => {
      const li = document.createElement("li");
      li.className = "task-item";

      // Формируем структуру с чекбоксом слева и кнопками справа
      li.innerHTML = `
                        <div class="task-left">
                            <input type="checkbox" ${task.status ? "checked" : ""} onchange="toggleTaskStatus('${task.id}', this.checked)">
                            <span class="${task.status ? "task-completed" : ""}">${task.text}</span>
                        </div>
                        <div class="task-buttons">
                            <button class="btn-edit" onclick="startEditTask('${task.id}', '${task.text.replace(/'/g, "\\'")}')">Изменить</button>
                            <button class="btn-delete" onclick="deleteTask('${task.id}')">Удалить</button>
                        </div>
                    `;
      taskList.appendChild(li);
    });
  } catch (error) {
    console.error("Ошибка при загрузке задач:", error);
  }
}

window.addEventListener("DOMContentLoaded", loadTasks);

// Распределитель клика по главной кнопке
function handleSubmit() {
  if (editingTaskId !== null) {
    saveEditedTask();
  } else {
    sendData();
  }
}

// Создание задачи (POST)
async function sendData() {
  const taskInput = document.getElementById("taskInput");
  const textValue = taskInput.value.trim();
  if (!textValue) return;

  try {
    const response = await fetch(`${BASE_URL}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: textValue }),
    });

    if (response.ok) {
      taskInput.value = "";
      loadTasks();
    }
  } catch (error) {
    console.error("Ошибка создания:", error);
  }
}

// Вход в режим редактирования по кнопке "Изменить"
function startEditTask(taskId, currentText) {
  editingTaskId = taskId;

  const taskInput = document.getElementById("taskInput");
  taskInput.placeholder = "Введите новый текст задачи";
  taskInput.value = currentText;
  taskInput.focus();

  document.getElementById("formTitle").innerText = "Редактировать задачу";
  document.getElementById("submitBtn").innerText = "Сохранить";
}

// Сохранение изменений текста (PATCH)
async function saveEditedTask() {
  const taskInput = document.getElementById("taskInput");
  const newText = taskInput.value.trim();
  if (!newText) return;

  try {
    const response = await fetch(`${BASE_URL}/tasks/${editingTaskId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: newText }),
    });

    if (response.ok) {
      editingTaskId = null;
      taskInput.value = "";
      taskInput.placeholder = "Введите текст задачи";

      document.getElementById("formTitle").innerText = "Создать новую задачу";
      document.getElementById("submitBtn").innerText = "Отправить";

      loadTasks();
    }
  } catch (error) {
    console.error("Ошибка обновления:", error);
  }
}

// Изменение статуса задачи (PATCH)
async function toggleTaskStatus(taskId, isChecked) {
  try {
    const response = await fetch(`${BASE_URL}/tasks/${taskId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: isChecked }),
    });

    if (response.ok) {
      loadTasks();
    }
  } catch (error) {
    console.error("Ошибка обновления статуса:", error);
  }
}

// Удаление задачи (DELETE)
async function deleteTask(taskId) {
  if (!confirm("Вы уверены, что хотите удалить эту задачу?")) return;

  try {
    const response = await fetch(`${BASE_URL}/tasks/${taskId}`, {
      method: "DELETE",
    });

    if (response.ok) {
      loadTasks();
    }
  } catch (error) {
    console.error("Ошибка удаления:", error);
  }
}
