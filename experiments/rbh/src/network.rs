use std::net::TcpStream;
use std::io::{Read, Write};
use serde::{Serialize, Deserialize};
use serde_json;
use crate::player::Player;

pub struct NetworkManager {
    stream: TcpStream,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Vector2(pub f32, pub f32);

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct PlayerState {
    pub id: u32,
    pub position: Vector2,
    pub health: f32,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct BulletState {
    pub position: Vector2,
    pub velocity: Vector2,
    pub bullet_type: String,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct EnemyState {
    pub id: u32,
    pub position: Vector2,
    pub enemy_type: String,
    pub health: f32,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct GameState {
    pub players: Vec<PlayerState>,
    pub enemies: Vec<EnemyState>,
    pub bullets: Vec<BulletState>,
    pub wave: u32,
}

impl NetworkManager {
    pub fn new(address: &str) -> Self {
        let stream = TcpStream::connect(address).unwrap();
        NetworkManager { stream }
    }

    pub fn send_player_state(&mut self, player: &Player) {
        let state = PlayerState {
            id: player.id,
            position: Vector2(player.position.x, player.position.y),
            health: player.health,
        };
        let serialized = serde_json::to_string(&state).unwrap();
        self.stream.write_all(serialized.as_bytes()).unwrap();
    }

    pub fn receive_game_state(&mut self) -> Option<GameState> {
        let mut buffer = [0; 16384]; // Increased buffer size
        match self.stream.read(&mut buffer) {
            Ok(n) => {
                if n > 0 {
                    let serialized = String::from_utf8_lossy(&buffer[..n]);
                    match serde_json::from_str::<GameState>(&serialized) {
                        Ok(game_state) => Some(game_state),
                        Err(e) => {
                            eprintln!("Failed to parse game state: {}", e);
                            None
                        }
                    }
                } else {
                    None
                }
            }
            Err(e) => {
                eprintln!("Failed to receive game state: {}", e);
                None
            }
        }
    }

    pub fn send_bullet(&mut self, bullet: &BulletState) {
        let serialized = serde_json::to_string(bullet).unwrap();
        self.stream.write_all(serialized.as_bytes()).unwrap();
    }
}