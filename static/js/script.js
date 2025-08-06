console.log("Javascript is loaded.");

function toggleDarkMode(target) {
	// document.body.classList.toggle("dark-mode");
	const container = document.getElementById(target);
	if (target == 'body') {
		document.body.classList.toggle("dark-mode");
	}
	else if (container) {
		container.classList.toggle("dark-mode");
	}
	console.log("Toggling dark mode");
}


function updateTime() {
	const now = new Date();
	const timeString = now.toLocaleTimeString();
	document.getElementById("time").textContent = timeString;
}

setInterval(updateTime, 1000);
updateTime();
