const canvas = document.getElementById('space-canvas');
const ctx = canvas.getContext('2d');

let stars = [];
const numStars = 100;
const starColors = ['#ffffff', '#00f0ff', '#ff0055', '#ffff00'];

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Генерируем пиксельные квадратные звезды
for (let i = 0; i < numStars; i++) {
    stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() > 0.85 ? 3 : 2, // Квадратные пиксели
        speed: Math.random() * 0.6 + 0.2,   // Медленный аркадный скролл
        color: starColors[Math.floor(Math.random() * starColors.length)]
    });
}

function animate() {
    ctx.fillStyle = 'rgba(3, 3, 8, 0.3)'; // Легкий шлейф движения
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    stars.forEach(star => {
        ctx.fillStyle = star.color;
        ctx.fillRect(Math.floor(star.x), Math.floor(star.y), star.size, star.size);

        star.y += star.speed;
        if (star.y > canvas.height) {
            star.y = 0;
            star.x = Math.random() * canvas.width;
        }
    });

    requestAnimationFrame(animate);
}

animate();