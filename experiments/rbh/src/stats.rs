pub struct Stats {
    pub max_health: f32,
    pub speed: f32,
    pub damage: f32,
    pub fire_rate: f32,
    pub speed_multiplier: f32,
    pub damage_multiplier: f32,
}

impl Default for Stats {
    fn default() -> Self {
        Stats {
            max_health: 100.0,
            speed: 5.0,
            damage: 10.0,
            fire_rate: 0.2,
            speed_multiplier: 1.0,
            damage_multiplier: 1.0,
        }
    }
}

#[derive(Clone, Copy)]
pub struct GameStats {
    pub enemies_killed: u32,
    pub wave: u32,
    pub spawn_timer: f32,
}

impl Default for GameStats {
    fn default() -> Self {
        GameStats {
            enemies_killed: 0,
            wave: 1,
            spawn_timer: 0.0,
        }
    }
}