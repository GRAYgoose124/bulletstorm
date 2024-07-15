use std::collections::VecDeque;
use crate::enemy::EnemyType;

pub struct Level {
    pub level_number: u32,
    pub wave_number: u32,
    waves: Vec<Wave>,
}

struct Wave {
    enemies: Vec<(EnemyType, f32)>,
}

impl Level {
    pub fn new(level_number: u32) -> Self {
        Level {
            level_number,
            wave_number: 0,
            waves: Self::generate_waves(level_number),
        }
    }

    fn generate_waves(level_number: u32) -> Vec<Wave> {
        let mut waves = Vec::new();
        let num_waves = 3 + level_number.min(5);

        for wave_index in 0..num_waves {
            let mut enemies = Vec::new();
            let num_enemies = 5 + wave_index * 2 + level_number * 2;

            for i in 0..num_enemies {
                let enemy_type = match (i + wave_index) % 5 {
                    0 => EnemyType::Basic,
                    1 => EnemyType::Sniper,
                    2 => EnemyType::Shotgun,
                    3 => EnemyType::Sine,
                    _ => if wave_index == num_waves - 1 && i == num_enemies - 1 {
                        EnemyType::Boss
                    } else {
                        EnemyType::Basic
                    },
                };
                enemies.push((enemy_type, i as f32 * 1.5));
            }

            waves.push(Wave { enemies });
        }

        waves
    }

    pub fn next_wave(&mut self) -> bool {
        self.wave_number += 1;
        self.wave_number <= self.waves.len() as u32
    }

    pub fn generate_spawn_queue(&self, difficulty: f32) -> VecDeque<(EnemyType, f32)> {
        if let Some(wave) = self.waves.get(self.wave_number as usize - 1) {
            wave.enemies
                .iter()
                .map(|(enemy_type, spawn_time)| (enemy_type, spawn_time / difficulty.sqrt()))
                .collect()
        } else {
            VecDeque::new()
        }
    }

    pub fn is_completed(&self) -> bool {
        self.wave_number > self.waves.len() as u32
    }
}