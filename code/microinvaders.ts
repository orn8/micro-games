let score: number = 0;
let playerX: number = 2;
let bullets: { x: number, y: number }[] = [];
let enemies: { x: number, y: number, health: number }[] = [];
let gameover: boolean = false;
let timer: number = 0;
let wave: number = 1;

function resetGame() {
    score = 0;
    bullets = [];
    playerX = 2;
    enemies = [];
    gameover = false;
    timer = 0;
    wave = 1;
}

function spawnEnemies() {
    // Generate random positions for the enemies
    for (let i = 0; i < 7; i++) {
        const enemy = {
            x: Math.randomRange(0, 4),
            y: -i,
            health: 2 + wave
        };
        enemies.push(enemy);
    }
}

function updateGame() {
    // Game Over
    if (gameover) {
        basic.clearScreen();
        basic.showString("SCORE");
        basic.showNumber(score);

        // Reset the game state
        resetGame();
        return;
    }

    // Player control
    if (input.isGesture(Gesture.TiltLeft) && playerX > 0) {
        playerX -= 1;
    } else if (input.isGesture(Gesture.TiltRight) && playerX < 4) {
        playerX += 1;
    }

    // Move the bullets
    bullets = bullets.filter(function (bullet: { x: number, y: number }) {
        bullet.y -= 1;
        if (bullet.y < 0) {
            return false;
        }
        return true;
    });

    // Collision detection
    for (const bullet of bullets) {
        for (const enemy of enemies) {
            if (bullet.x === enemy.x && bullet.y === enemy.y) {
                enemy.health -= 1;
                if (enemy.health <= 0) {
                    // Enemy destroyed
                    score += 1;
                    enemies.removeElement(enemy);
                }
                bullets.removeElement(bullet);
                break;
            }
        }
    }

    // Check if enemies reached the bottom
    for (const enemy of enemies) {
        if (enemy.y === 4) {
            gameover = true;
            break;
        } else {
            enemy.y += 1;
        }
    }

    // Spawn new wave if all enemies are destroyed
    if (enemies.length === 0) {
        wave += 1;
        spawnEnemies();
    }

    // Display objects on screen
    basic.clearScreen();
    led.plot(playerX, 4);
    for (const enemy of enemies) {
        led.plot(enemy.x, enemy.y);
    }
    for (const bullet of bullets) {
        led.plot(bullet.x, bullet.y);
    }
}

// Shoot bullet
input.onButtonPressed(Button.B, function () {
    bullets.push({ x: playerX, y: 3 });
    music.playTone(Note.C, 100);
});

// Game loop
basic.forever(function () {
    updateGame();

    // Delay to control game speed
    basic.pause(1000); // Change delay to 1000 milliseconds (1 second)

    // Update timer
    timer += 1;

    // Spawn new wave every 7 seconds
    if (timer % 7 === 0) {
        if (enemies.length === 0) {
            spawnEnemies();
        }
    }
});