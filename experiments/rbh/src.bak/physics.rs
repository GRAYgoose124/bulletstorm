use raylib::prelude::*;

pub trait Collidable {
    fn collides_with_circle(&self, center: Vector2, radius: f32) -> bool;
}

// Helper function for circle-circle collision
pub fn circle_circle_collision(center1: Vector2, radius1: f32, center2: Vector2, radius2: f32) -> bool {
    center1.distance_to(center2) < (radius1 + radius2)
}

// Helper function for point-circle collision
pub fn point_circle_collision(point: Vector2, circle_center: Vector2, circle_radius: f32) -> bool {
    point.distance_to(circle_center) < circle_radius
}