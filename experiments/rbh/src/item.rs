use std::rc::Rc;

use crate::enemy::ShotPattern;
use crate::stats::Stats;
use crate::player::{Effect, EffectType};

#[derive(Clone, Copy, Eq, Hash, PartialEq, Debug)]
pub enum ItemSlot {
    Weapon,
    Helmet,
    Chest,
    Gloves,
    Boots,
    Ring1,
    Ring2,
    Amulet,
}

#[derive(Clone)]
pub struct Item {
    pub name: String,
    pub slot: ItemSlot,
    pub stats: Stats,
    pub effects: Vec<Effect>,
    pub abilities: Vec<Ability>,
}

#[derive(Clone)]
pub enum Ability {
    ModifyShot(ShotPattern),
    OnHit(Rc<dyn Fn() -> Effect>),
    OnMove(Rc<dyn Fn() -> Effect>),
}

impl Item {
    pub fn new(name: String, slot: ItemSlot, stats: Stats, effects: Vec<Effect>, abilities: Vec<Ability>) -> Self {
        Item { name, slot, stats, effects, abilities }
    }
}

pub fn create_sample_items() -> Vec<Item> {
    vec![
        Item::new(
            "Basic Sword".to_string(),
            ItemSlot::Weapon,
            Stats { damage: 5.0, ..Default::default() },
            vec![],
            vec![Ability::ModifyShot(ShotPattern::Single)],
        ),
        Item::new(
            "Fire Staff".to_string(),
            ItemSlot::Weapon,
            Stats { damage: 3.0, fire_rate: -0.1, ..Default::default() },
            vec![],
            vec![
                Ability::ModifyShot(ShotPattern::Spread(3)),
                Ability::OnHit(Rc::new(|| Effect { effect_type: EffectType::Burning, duration: 3.0 })),
            ],
        ),
        Item::new(
            "Leather Helmet".to_string(),
            ItemSlot::Helmet,
            Stats { max_health: 20.0, ..Default::default() },
            vec![],
            vec![],
        ),
        Item::new(
            "Speed Boots".to_string(),
            ItemSlot::Boots,
            Stats { speed: 1.0, ..Default::default() },
            vec![],
            vec![],
        ),
    ]
}