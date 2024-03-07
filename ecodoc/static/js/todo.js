document.addEventListener("DOMContentLoaded", function () {
    const taskInput = document.getElementById("taskInput");
    const addTaskButton = document.getElementById("addTask");
    const taskList = document.getElementById("taskList");
    let tasks = getTasksFromLocalStorage();

    // Load tasks from localStorage
    loadTasks();

    addTaskButton.addEventListener("click", function () {
        const taskText = taskInput.value;
        if (taskText.trim() !== "") {
            addTaskToDOM(taskText);
            taskInput.value = "";
            tasks.push(taskText);
            saveTasksToLocalStorage(tasks);
        }
    });

    function addTaskToDOM(taskText) {
        const li = document.createElement("li");
        li.innerHTML = `
            <span>${taskText}</span>
            <button>Delete</button>
        `;
        taskList.appendChild(li);

        const deleteButton = li.querySelector("button");
        deleteButton.addEventListener("click", function () {
            li.remove();
            const index = tasks.indexOf(taskText);
            if (index !== -1) {
                tasks.splice(index, 1);
                saveTasksToLocalStorage(tasks);
            }
        });
    }

    function saveTasksToLocalStorage(taskArray) {
        localStorage.setItem("tasks", JSON.stringify(taskArray));
    }

    function loadTasks() {
        tasks.forEach(function (taskText) {
            addTaskToDOM(taskText);
        });
    }

    function getTasksFromLocalStorage() {
        const storedTasks = localStorage.getItem("tasks");
        if (storedTasks) {
            return JSON.parse(storedTasks);
        } else {
            return [];
        }
    }
});
