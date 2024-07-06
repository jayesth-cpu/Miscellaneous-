import kaboom from "kaboom";

// Initialize the game context
kaboom();

// Load assets
loadSprite("coin", "https://kaboomjs.com/sprites/coin.png");
loadSpriteAtlas("https://kaboomjs.com/sprites/dungeon.png", {
    "hero": {
        x: 128,
        y: 196,
        width: 144,
        height: 28,
        sliceX: 9,
        anims: {
            idle: {
                from: 0,
                to: 3,
                loop: true,
                speed: 5
            },
            run: {
                from: 4,
                to: 7,
                loop: true,
                speed: 10
            },
        },
    },
});

// Define some constants
const MOVE_SPEED = 200;
const JUMP_FORCE = 550;

// Game scene
scene("game", () => {
    // Add a game object to screen
    const player = add([
        sprite("hero"),
        pos(80, 40),
        area(),
        body(),
        scale(2),
    ]);

    // Start with idle animation
    player.play("idle");

    // Add platform
    add([
        rect(width(), 48),
        pos(0, height() - 48),
        outline(4),
        area(),
        solid(),
        color(127, 200, 255),
    ]);

    // Add some coins
    function spawnCoin() {
        add([
            sprite("coin"),
            pos(rand(0, width()), height() - 64),
            area(),
            "coin"
        ]);
    }

    // Spawn a coin every second
    loop(1, () => {
        spawnCoin();
    });

    // Define player movements
    onKeyDown("left", () => {
        player.move(-MOVE_SPEED, 0);
        player.scale.x = -2;
        if (player.curAnim() !== "run") {
            player.play("run");
        }
    });

    onKeyDown("right", () => {
        player.move(MOVE_SPEED, 0);
        player.scale.x = 2;
        if (player.curAnim() !== "run") {
            player.play("run");
        }
    });

    onKeyRelease(["left", "right"], () => {
        if (!isKeyDown("left") && !isKeyDown("right")) {
            player.play("idle");
        }
    });

    onKeyPress("space", () => {
        if (player.isGrounded()) {
            player.jump(JUMP_FORCE);
        }
    });

    // Lose if you fall off the screen
    player.onUpdate(() => {
        if (player.pos.y >= height()) {
            go("lose");
        }
    });

    // Collect coins
    let score = 0;
    const scoreLabel = add([
        text(score),
        pos(24, 24),
    ]);

    onCollide("coin", "hero", (coin) => {
        destroy(coin);
        score++;
        scoreLabel.text = score;
    });
});

// Lose scene
scene("lose", () => {
    add([
        text("Game Over"),
        pos(center()),
        origin("center"),
    ]);

    onKeyPress("space", () => {
        go("game");
    });
});

// Start the game
go("game");