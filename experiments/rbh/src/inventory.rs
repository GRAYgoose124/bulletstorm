pub struct Inventory {
    items: Vec<Item>,
    capacity: usize,
}

impl Inventory {
    pub fn new() -> Self {
        Inventory {
            items: Vec::new(),
            capacity: 10,
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

    // ... other inventory management methods ...
}

