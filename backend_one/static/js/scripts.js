window.addEventListener('scroll', function() {
	const header = document.getElementById('header');
	if (window.scrollY > 100) {
	  header.classList.add('visible');
	} else {
	  header.classList.remove('visible');
	}
  });
  
  document.addEventListener('DOMContentLoaded', function() {
	const chatButton = document.getElementById('chat-button');
	const chatWindow = document.getElementById('chat-window');
	const closeChat = document.getElementById('close-chat');
	
	chatButton.addEventListener('click', function() {
	  chatWindow.style.display = 'flex';
	});
	
	closeChat.addEventListener('click', function() {
	  chatWindow.style.display = 'none';
	});
	
	document.addEventListener('click', function(event) {
	  if (!chatWindow.contains(event.target)) {
		if (event.target !== chatButton) {
		  chatWindow.style.display = 'none';
		}
	  }
	});
	
	socket.on('getAllTasks', (tasks) => {
		taskList.innerHTML = '';
		tasks.forEach(task => displayTask(task));
	  });
  });