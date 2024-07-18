use std::net::TcpStream;
use std::io::{Read, Write};
use serde::{Serialize, Deserialize};
use serde_json;
use raylib::math::Vector2 as RaylibVector2;

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Vector2(pub f32, pub f32);

impl From<RaylibVector2> for Vector2 {
    fn from(v: RaylibVector2) -> Self {
        Vector2(v.x, v.y)
    }
}

impl Into<RaylibVector2> for Vector2 {
    fn into(self) -> RaylibVector2 {
        RaylibVector2::new(self.0, self.1)
    }
}

pub struct NetworkManager {
    stream: TcpStream,
}

#[derive(Clone, Serialize, Deserialize, Debug)]
pub struct PlayerState {
    pub id: u32,
    pub position: Vector2,
    pub health: f32,
}

#[derive(Clone, Serialize, Deserialize, Debug)]
pub struct EnemyState {
    pub id: u32,
    pub position: Vector2,
    pub enemy_type: String,
    pub health: f32,
    pub speed: f32,
    pub shoot_timer: f32,
    pub shoot_interval: f32,
}

#[derive(Clone, Serialize, Deserialize, Debug)]
pub struct BulletState {
    pub position: Vector2,
    pub velocity: Vector2,
    pub bullet_type: String,
}

#[derive(Clone, Serialize, Deserialize, Debug)]
pub struct GameState {
    pub players: Vec<PlayerState>,
    pub enemies: Vec<EnemyState>,
    pub bullets: Vec<BulletState>,
    pub wave: u32,
}

#[derive(Serialize, Deserialize, Debug)]
pub enum PlayerAction {
    Move(Vector2),
    Shoot(Vector2),
}

impl NetworkManager {
    pub fn new(address: &str) -> Result<Self, std::io::Error> {
        let stream = TcpStream::connect(address)?;
        Ok(NetworkManager { stream })
    }

    pub fn send_player_action(&mut self, action: PlayerAction) -> Result<(), std::io::Error> {
        let serialized = serde_json::to_string(&action)?;
        self.stream.write_all(serialized.as_bytes())?;
        self.stream.flush()?;
        Ok(())
    }

    pub fn receive_game_state(&mut self) -> Result<GameState, std::io::Error> {
        let mut buffer = [0; 65536]; // Increased buffer size
        let bytes_read = self.stream.read(&mut buffer)?;
        
        if bytes_read == 0 {
            return Err(std::io::Error::new(std::io::ErrorKind::ConnectionAborted, "Server disconnected"));
        }

        let serialized = String::from_utf8_lossy(&buffer[..bytes_read]);
        match serde_json::from_str::<GameState>(&serialized) {
            Ok(game_state) => Ok(game_state),
            Err(e) => Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!("Failed to parse game state: {}", e))),
        }
    }
}

// Utility functions to convert between raylib Vector2 and our network Vector2
pub fn to_network_vector(v: raylib::math::Vector2) -> Vector2 {
    Vector2(v.x, v.y)
}

pub fn from_network_vector(v: Vector2) -> raylib::math::Vector2 {
    raylib::math::Vector2::new(v.0, v.1)
}