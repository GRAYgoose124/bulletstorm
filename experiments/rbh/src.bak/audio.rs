use raylib::prelude::*;

pub enum MusicTrack {
    MainMenu,
    GamePlay,
    Boss,
}

pub enum SoundEffect {
    PlayerShoot,
    EnemyShoot,
    PlayerHit,
    EnemyDeath,
    ItemPickup,
    LevelUp,
    GameOver,
}

pub struct AudioManager {
    music: [Music; 3],
    sound_effects: [Sound; 7],
    current_music: Option<MusicTrack>,
}

impl AudioManager {
    pub fn new(rl: &mut RaylibHandle) -> Self {
        rl.init_audio_device();

        let music = [
            rl.load_music("assets/music/main_menu.ogg").unwrap(),
            rl.load_music("assets/music/gameplay.ogg").unwrap(),
            rl.load_music("assets/music/boss.ogg").unwrap(),
        ];

        let sound_effects = [
            rl.load_sound("assets/sfx/player_shoot.wav").unwrap(),
            rl.load_sound("assets/sfx/enemy_shoot.wav").unwrap(),
            rl.load_sound("assets/sfx/player_hit.wav").unwrap(),
            rl.load_sound("assets/sfx/enemy_death.wav").unwrap(),
            rl.load_sound("assets/sfx/item_pickup.wav").unwrap(),
            rl.load_sound("assets/sfx/level_up.wav").unwrap(),
            rl.load_sound("assets/sfx/game_over.wav").unwrap(),
        ];

        AudioManager {
            music,
            sound_effects,
            current_music: None,
        }
    }

    pub fn play_music(&mut self, track: MusicTrack) {
        if self.current_music != Some(track) {
            if let Some(current) = self.current_music {
                self.music[current as usize].stop();
            }
            self.music[track as usize].play();
            self.current_music = Some(track);
        }
    }

    pub fn play_sound(&self, effect: SoundEffect) {
        self.sound_effects[effect as usize].play();
    }

    pub fn update(&mut self) {
        if let Some(current) = self.current_music {
            self.music[current as usize].update();
        }
    }
}s