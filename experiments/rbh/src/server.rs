use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};
use std::thread;
use std::sync::{Arc, Mutex};
use std::collections::HashMap;
use serde::{Serialize, Deserialize};
use rand::{thread_rng, Rng};

const TICK_RATE: f32 = 60.0;
const WINDOW_WIDTH: f32 = 1280.0;
const WINDOW_HEIGHT: f32 = 720.0;

#[derive(Clone, Serialize, Deserialize)]
struct Vector2 {
    x: f32,
    y: f32,
}

#[derive(Clone, Serialize, Deserialize)]
struct PlayerState {
    id: u32,
    position: Vector2,
    health: f32,
}

#[derive(Clone, Serialize, Deserialize)]
struct EnemyState {
    id: u32,
    position: Vector2,
    enemy_type: String,
    health: f32,
}

#[derive(Clone, Serialize, Deserialize)]
struct BulletState {
    position: Vector2,
    velocity: Vector2,
    bullet_type: String,
}

#[derive(Clone, Serialize, Deserialize)]
struct GameState {
    players: HashMap<u32, PlayerState>,
    enemies: Vec<EnemyState>,
    bullets: Vec<BulletState>,
    wave: u32,
}

struct Client {
    stream: TcpStream,
    player_id: u32,
}

struct Server {
    clients: HashMap<u32, Client>,
    game_state: GameState,
    next_player_id: u32,
    next_enemy_id: u32,
}

impl Server {
    fn new() -> Self {
        Server {
            clients: HashMap::new(),
            game_state: GameState {
                players: HashMap::new(),
                enemies: Vec::new(),
                bullets: Vec::new(),
                wave: 1,
            },
            next_player_id: 1,
            next_enemy_id: 1,
        }
    }

    fn add_client(&mut self, stream: TcpStream) -> u32 {
        let player_id = self.next_player_id;
        self.next_player_id += 1;

        let client = Client { stream, player_id };
        self.clients.insert(player_id, client);

        let player_state = PlayerState {
            id: player_id,
            position: Vector2 { x: WINDOW_WIDTH / 2.0, y: WINDOW_HEIGHT - 50.0 },
            health: 100.0,
        };
        self.game_state.players.insert(player_id, player_state);

        player_id
    }

    fn remove_client(&mut self, player_id: u32) {
        self.clients.remove(&player_id);
        self.game_state.players.remove(&player_id);
    }

    fn update(&mut self) {
        self.update_enemies();
        self.update_bullets();
        self.spawn_enemies();
        self.check_collisions();
    }

    fn update_enemies(&mut self) {
        for enemy in &mut self.game_state.enemies {
            // Simple enemy movement logic
            enemy.position.y += 1.0;
            if enemy.position.y > WINDOW_HEIGHT {
                enemy.position.y = 0.0;
            }
        }
    }

    fn update_bullets(&mut self) {
        self.game_state.bullets.retain_mut(|bullet| {
            bullet.position.x += bullet.velocity.x;
            bullet.position.y += bullet.velocity.y;
            bullet.position.x >= 0.0 && bullet.position.x <= WINDOW_WIDTH && 
            bullet.position.y >= 0.0 && bullet.position.y <= WINDOW_HEIGHT
        });
    }

    fn spawn_enemies(&mut self) {
        let mut rng = thread_rng();
        if self.game_state.enemies.len() < self.game_state.wave as usize * 2 {
            let enemy = EnemyState {
                id: self.next_enemy_id,
                position: Vector2 { x: rng.gen_range(0.0..WINDOW_WIDTH), y: 0.0 },
                enemy_type: "Basic".to_string(),
                health: 50.0,
            };
            self.game_state.enemies.push(enemy);
            self.next_enemy_id += 1;
        }
    }

    fn check_collisions(&mut self) {
        // Simplified collision detection
        for bullet in &self.game_state.bullets {
            if bullet.bullet_type == "Player" {
                self.game_state.enemies.retain_mut(|enemy| {
                    let dx = bullet.position.x - enemy.position.x;
                    let dy = bullet.position.y - enemy.position.y;
                    let distance = (dx * dx + dy * dy).sqrt();
                    if distance < 30.0 {  // Assuming enemy radius is 30
                        enemy.health -= 10.0;
                    }
                    enemy.health > 0.0
                });
            } else {
                for player in self.game_state.players.values_mut() {
                    let dx = bullet.position.x - player.position.x;
                    let dy = bullet.position.y - player.position.y;
                    let distance = (dx * dx + dy * dy).sqrt();
                    if distance < 20.0 {  // Assuming player radius is 20
                        player.health -= 5.0;
                    }
                }
            }
        }
    }

    fn broadcast_state(&mut self) {
        let state_json = serde_json::to_string(&self.game_state).unwrap();
        for client in self.clients.values_mut() {
            if let Err(e) = client.stream.write_all(state_json.as_bytes()) {
                eprintln!("Failed to send state to client {}: {}", client.player_id, e);
            }
        }
    }

    fn handle_client_message(&mut self, player_id: u32, message: &str) {
        if let Ok(player_state) = serde_json::from_str::<PlayerState>(message) {
            if let Some(current_state) = self.game_state.players.get_mut(&player_id) {
                current_state.position = player_state.position;
            }
        } else if let Ok(bullet) = serde_json::from_str::<BulletState>(message) {
            self.game_state.bullets.push(bullet);
        }
    }
}

fn handle_client(server: Arc<Mutex<Server>>, mut stream: TcpStream) {
    let player_id = {
        let mut server = server.lock().unwrap();
        server.add_client(stream.try_clone().unwrap())
    };

    println!("New client connected: {}", player_id);

    let mut buffer = [0; 1024];
    loop {
        match stream.read(&mut buffer) {
            Ok(0) => {
                println!("Client {} disconnected", player_id);
                let mut server = server.lock().unwrap();
                server.remove_client(player_id);
                break;
            }
            Ok(n) => {
                let message = String::from_utf8_lossy(&buffer[..n]);
                let mut server = server.lock().unwrap();
                server.handle_client_message(player_id, &message);
            }
            Err(e) => {
                eprintln!("Failed to read from client {}: {}", player_id, e);
                let mut server = server.lock().unwrap();
                server.remove_client(player_id);
                break;
            }
        }
    }
}

fn main() {
    let server = Arc::new(Mutex::new(Server::new()));
    let listener = TcpListener::bind("127.0.0.1:8080").unwrap();
    println!("Server listening on port 8080");

    let server_clone = Arc::clone(&server);
    thread::spawn(move || {
        let mut last_update = std::time::Instant::now();
        loop {
            let now = std::time::Instant::now();
            let dt = now.duration_since(last_update).as_secs_f32();
            if dt >= 1.0 / TICK_RATE {
                let mut server = server_clone.lock().unwrap();
                server.update();
                server.broadcast_state();
                last_update = now;
            }
            std::thread::sleep(std::time::Duration::from_millis(1));
        }
    });

    for stream in listener.incoming() {
        let stream = stream.unwrap();
        let server = Arc::clone(&server);
        thread::spawn(move || {
            handle_client(server, stream);
        });
    }
}