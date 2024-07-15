use crate::item::Item;

pub struct Inventory {
    items: Vec<Item>,
    capacity: usize,
}

impl Inventory {
    pub fn new(capacity: usize) -> Self {
        Inventory {
            items: Vec::new(),
            capacity,
        }
    }

    pub fn add_item(&mut self, item: Item) -> bool {
        if self.items.len() < self.capacity {
            self.items.push(item);
            true
        } else {
            false
        }
    }

    pub fn remove_item(&mut self, index: usize) -> Option<Item> {
        if index < self.items.len() {
            Some(self.items.remove(index))
        } else {
            None
        }
    }

    pub fn get_items(&self) -> &[Item] {
        &self.items
    }
}