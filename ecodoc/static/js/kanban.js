window.addEventListener('load', () => {
    loadTasks();
});

const tasks = [];
const columns = document.querySelectorAll('.tasks');
const taskModal = document.getElementById('task-modal');
const taskNameInput = document.getElementById('task-name');
const taskDeadlineInput = document.getElementById('task-deadline');
const closeModalButton = document.querySelector('.close');
const addTaskButton = document.querySelector('.add-task-button');

columns.forEach(column => {
    column.addEventListener('dragover', (event) => {
        event.preventDefault();
    });

    column.addEventListener('drop', (event) => {
        event.preventDefault();
        const taskId = event.dataTransfer.getData('text/plain');
        const task = document.getElementById(taskId);
        const columnIndex = getColumnIndex(column);
        moveTaskToColumn(taskId, columnIndex);
        column.appendChild(task);
    });
});

function allowDrop(event) {
    event.preventDefault();
}

function openModal() {
    taskModal.style.display = 'block';
}

function closeModal() {
    taskModal.style.display = 'none';
}

function addTask() {
    const taskName = document.getElementById('task-name').value;
    const taskDescription = document.getElementById('task-description').value;
    const taskDeadline = document.getElementById('task-deadline').value;

    if (taskName.trim() !== '' && taskDeadline.trim() !== '') {
        const task = {
            id: 'task' + tasks.length,
            name: taskName,
            description: taskDescription,
            deadline: taskDeadline,
            column: 0 // Set the column property initially to 0 or the appropriate index
        };

        tasks.push(task);

        const todoColumn = document.getElementById('todo');
        todoColumn.appendChild(createTaskElement(task));

        $.ajax({
            url: '/kanban_add/',  // URL of the Django view function
            type: 'POST',          // HTTP method
            data: task,            // Task data to be passed to the view
            success: function(response) {
                // Handle success response
                console.log(response);
                // Assuming the response is some indicator of success
                // Perform further actions as needed
            },
            error: function(xhr, status, error) {
                // Handle errors
                console.error(xhr.responseText);
            }
        });
        saveTasksToLocalStorage(tasks);

        closeModal();

    }
}
// Save tasks to localStorage
function saveTasksToLocalStorage(taskArray) {
    localStorage.setItem('tasks', JSON.stringify(taskArray));
    console.log('Tasks saved to localStorage:', taskArray);
}


// Load tasks from localStorage
function loadTasks() {
    const savedTasks = localStorage.getItem('tasks');
    if (savedTasks) {
        tasks.length = 0; // Clear the current task array
        const parsedTasks = JSON.parse(savedTasks);
        parsedTasks.forEach(task => {
            tasks.push(task);
            const columnId = getColumnIdForTask(task);
            const column = document.getElementById(columnId);
            column.appendChild(createTaskElement(task));
        });
    }
}

// Create a new task element with the given data
function createTaskElement(task) {
    const taskElement = document.createElement('div');
    taskElement.className = 'task';
    taskElement.id = task.id;
    taskElement.draggable = true;
    taskElement.innerHTML = `<strong>${task.name}</strong><br>${task.description}<br>Deadline: ${task.deadline}`;
    taskElement.addEventListener('dragstart', (event) => {
        event.dataTransfer.setData('text/plain', event.target.id);
    });
    taskElement.addEventListener('dblclick', () => {
        yn=confirm("Do you want to delete the task?")
        if(yn){
            taskElement.remove();
        }
       
        // Remove the task from the tasks array
        const index = tasks.findIndex(item => item.id === task.id);
        if (index !== -1) {
            tasks.splice(index, 1);
        }
        saveTasksToLocalStorage(tasks); // Update localStorage
    });

    return taskElement;
}

// Get the column index for a given element
function getColumnIndex(column) {
    return Array.from(columns).indexOf(column);
}

// Move a task to a new column
function moveTaskToColumn(taskId, columnIndex) {
    const task = tasks.find(item => item.id === taskId);
    if (task) {
        task.column = columnIndex;
        saveTasksToLocalStorage(tasks);
    }
}

// Get the column ID for a given task
function getColumnIdForTask(task) {
    if (columns.length === 0 || task.column === undefined || task.column < 0 || task.column >= columns.length) {
        console.error('Invalid task or columns array.');
        return null;
    }
    return columns[task.column].id;
}



