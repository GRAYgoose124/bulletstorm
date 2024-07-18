use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};
use std::thread;
use std::sync::{Arc, Mutex};
use std::collections::HashMap;
use serde::{Serialize, Deserialize};
use serde_json;
use rand::{thread_rng, Rng};

mod network;

use network::{Vector2, PlayerAction, GameState, PlayerState, EnemyState, BulletState};

const TICK_RATE: f32 = 60.0;
const WINDOW_WIDTH: f32 = 1280.0;
const WINDOW_HEIGHT: f32 = 720.0;
const ENEMY_BULLET_SPEED: f32 = 200.0;
const PLAYER_BULLET_SPEED: f32 = 300.0;

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
                players: Vec::new(),
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
            position: Vector2(WINDOW_WIDTH / 2.0, WINDOW_HEIGHT - 50.0),
            health: 100.0,
        };
        self.game_state.players.push(player_state);

        player_id
    }

    fn remove_client(&mut self, player_id: u32) {
        self.clients.remove(&player_id);
        self.game_state.players.retain(|p| p.id != player_id);
    }

    fn update(&mut self, delta_time: f32) {
        self.update_enemies(delta_time);
        self.update_bullets(delta_time);
        self.spawn_enemies();
        self.check_collisions();
    }
    
    fn update_enemies(&mut self, delta_time: f32) {
        let directions: Vec<(f32, f32)> = self.game_state.enemies
            .iter()
            .map(|enemy| self.get_direction_to_nearest_player(enemy.position.clone()))
            .collect();

        let mut new_bullets = Vec::new();

        for (enemy, direction) in self.game_state.enemies.iter_mut().zip(directions.iter()) {
            enemy.position.1 += enemy.speed * delta_time;
            if enemy.position.1 > WINDOW_HEIGHT {
                enemy.position.1 = 0.0;
            }

            enemy.shoot_timer -= delta_time;
            if enemy.shoot_timer <= 0.0 {
                enemy.shoot_timer = enemy.shoot_interval;
                let bullet = BulletState {
                    position: enemy.position.clone(),
                    velocity: Vector2(direction.0 * ENEMY_BULLET_SPEED, direction.1 * ENEMY_BULLET_SPEED),
                    bullet_type: "Enemy".to_string(),
                };
                new_bullets.push(bullet);
            }
        }

        self.game_state.bullets.extend(new_bullets);
    }

    fn get_direction_to_nearest_player(&self, enemy_pos: Vector2) -> (f32, f32) {
        if let Some(player) = self.game_state.players.first() {
            let dx = player.position.0 - enemy_pos.0;
            let dy = player.position.1 - enemy_pos.1;
            let magnitude = (dx * dx + dy * dy).sqrt();
            (dx / magnitude, dy / magnitude)
        } else {
            (0.0, 1.0)
        }
    }

    fn update_bullets(&mut self, delta_time: f32) {
        self.game_state.bullets.retain_mut(|bullet| {
            bullet.position.0 += bullet.velocity.0 * delta_time;
            bullet.position.1 += bullet.velocity.1 * delta_time;
            bullet.position.0 >= 0.0 && bullet.position.0 <= WINDOW_WIDTH && 
            bullet.position.1 >= 0.0 && bullet.position.1 <= WINDOW_HEIGHT
        });
    }

    fn spawn_enemies(&mut self) {
        let mut rng = thread_rng();
        if self.game_state.enemies.len() < self.game_state.wave as usize * 2 {
            let enemy = EnemyState {
                id: self.next_enemy_id,
                position: Vector2(rng.gen_range(0.0..WINDOW_WIDTH), 0.0),
                enemy_type: "Basic".to_string(),
                health: 50.0,
                speed: 50.0,
                shoot_timer: 0.0,
                shoot_interval: 2.0,
            };
            self.game_state.enemies.push(enemy);
            self.next_enemy_id += 1;
        }
    }

    fn check_collisions(&mut self) {
        let mut enemies_to_remove = Vec::new();
        let mut bullets_to_remove = Vec::new();

        for (bullet_idx, bullet) in self.game_state.bullets.iter().enumerate() {
            match bullet.bullet_type.as_str() {
                "Enemy" => {
                    for player in &mut self.game_state.players {
                        let dx = bullet.position.0 - player.position.0;
                        let dy = bullet.position.1 - player.position.1;
                        let distance = (dx * dx + dy * dy).sqrt();
                        if distance < 20.0 {
                            player.health -= 10.0;
                            bullets_to_remove.push(bullet_idx);
                            break;
                        }
                    }
                }
                "Player" => {
                    for (enemy_idx, enemy) in self.game_state.enemies.iter_mut().enumerate() {
                        let dx = bullet.position.0 - enemy.position.0;
                        let dy = bullet.position.1 - enemy.position.1;
                        let distance = (dx * dx + dy * dy).sqrt();
                        if distance < 30.0 {
                            enemy.health -= 25.0;
                            bullets_to_remove.push(bullet_idx);
                            if enemy.health <= 0.0 {
                                enemies_to_remove.push(enemy_idx);
                            }
                            break;
                        }
                    }
                }
                _ => {}
            }
        }

        for idx in bullets_to_remove.into_iter().rev() {
            self.game_state.bullets.swap_remove(idx);
        }

        for idx in enemies_to_remove.into_iter().rev() {
            self.game_state.enemies.swap_remove(idx);
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
        if let Ok(player_action) = serde_json::from_str::<PlayerAction>(message) {
            match player_action {
                PlayerAction::Move(position) => {
                    if let Some(player) = self.game_state.players.iter_mut().find(|p| p.id == player_id) {
                        player.position = position;
                    }
                }
                PlayerAction::Shoot(direction) => {
                    if let Some(player) = self.game_state.players.iter().find(|p| p.id == player_id) {
                        let bullet = BulletState {
                            position: player.position.clone(),
                            velocity: Vector2(direction.0 * PLAYER_BULLET_SPEED, direction.1 * PLAYER_BULLET_SPEED),
                            bullet_type: "Player".to_string(),
                        };
                        self.game_state.bullets.push(bullet);
                    }
                }
            }
        } else {
            eprintln!("Received invalid message from client {}: {:?}", player_id, message);
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
                server.update(dt);
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