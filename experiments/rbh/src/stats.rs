#[derive(Clone, Copy)]
pub struct Stats {
    pub max_health: f32,
    pub speed: f32,
    pub damage: f32,
    pub fire_rate: f32,
    pub speed_multiplier: f32,
    pub damage_multiplier: f32,
    pub bullet_speed: f32,  // Add this line
}

impl Default for Stats {
    fn default() -> Self {
        Stats {
            max_health: 100.0,
            speed: 5.0,
            damage: 1.0,
            fire_rate: 0.2,
            speed_multiplier: 1.0,
            damage_multiplier: 1.0,
            bullet_speed: 300.0,  // Add this line
        }
    }
}

impl Stats {
    pub fn new(max_health: f32, speed: f32, damage: f32, fire_rate: f32, speed_multiplier: f32, damage_multiplier: f32, bullet_speed: f32) -> Self {
        Stats {
            max_health,
            speed,
            damage,
            fire_rate,
            speed_multiplier,
            damage_multiplier,
            bullet_speed
        }
    }

    pub fn add(&mut self, other: Stats) {
        self.max_health += other.max_health;
        self.speed += other.speed;
        self.damage += other.damage;
        self.fire_rate += other.fire_rate;
        self.speed_multiplier += other.speed_multiplier;
        self.damage_multiplier += other.damage_multiplier;
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