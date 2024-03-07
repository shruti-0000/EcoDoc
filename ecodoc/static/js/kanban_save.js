// Function to handle task drop event
function drop(event, columnId) {
    event.preventDefault();
    const taskId = event.dataTransfer.getData("task_id");
    const task = document.getElementById(taskId);
    task.parentNode.removeChild(task);
    const column = document.getElementById(columnId);
    column.appendChild(task);
}

// Function to allow dropping into a column
function allowDrop(event) {
    event.preventDefault();
}

// Function to handle "Save Changes" button click
function saveChanges() {
    const email = document.getElementById('email').value;
    const columns = document.querySelectorAll('.column');
    columns.forEach(column => {
        const columnId = column.id;
        const tasks = column.querySelectorAll('.task');
        tasks.forEach(task => {
            const taskId = task.id;
            const taskData = {
                name: task.dataset.name,
                description: task.dataset.description,
                deadline: task.dataset.deadline,
                column: columnId
            };
            // Save task data to Django view for saving to database
            fetch('/save_kanban_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ email: email, tasks: [taskData] })
            }).then(response => {
                // Handle response
                console.log(response);
            }).catch(error => {
                // Handle error
                console.error('Error:', error);
            });
        });
    });
}
