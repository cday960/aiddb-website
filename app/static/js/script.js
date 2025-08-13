console.log("Javascript is loaded.");

function toggleDarkMode(target) {
	const container = document.getElementById(target);


	if (target === 'body') {
		document.body.classList.toggle("dark-mode");
	}
	else if (container) {
		container.classList.toggle("dark-mode");
	}
	console.log("Toggling dark mode:", target);
}


function updateTime() {
	const time_el = document.getElementById("time");
	if (!time_el) return;
	time_el.textContent = new Date().toLocaleString();
}

// Bind all events once DOM is ready (no inline so CSP safe)
document.addEventListener("DOMContentLoaded", function() {
	// Bind all buttons that declare target to data-dark-toggle="..."
	document.querySelectorAll("[data-dark-toggle]").forEach(function(btn) {
		btn.addEventListener("click", function() {
			const target = btn.getAttribute("data-dark-toggle") || "body";
			toggleDarkMode(target);
		});
	});
	updateTime();
	setInterval(updateTime, 1000);
});

