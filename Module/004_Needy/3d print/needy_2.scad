width = 70;
height = 156;
thickness = 4;
$fn = 20;

difference() {
    cube([width, height, thickness], center = true);

   // SCREW HOLES
   screw_hole = 3.5/2;
   dist_boarder = 6.5;

   color([1,0,0])
      translate([(width/2-dist_boarder),(height/2-dist_boarder), 0])
         cylinder(h= height+1, r = screw_hole, center = true, $fn=100);

   color([1,0,0])
      translate([(width/2-dist_boarder)*-1,(height/2-dist_boarder), 0])
         cylinder(h= height+1, r = screw_hole, center = true, $fn=100);

   color([1,0,0])
      translate([(width/2-dist_boarder)*-1,(height/2-dist_boarder)*-1, 0])
         cylinder(h= height+1, r = screw_hole, center = true, $fn=100);

   color([1,0,0])
      translate([(width/2-dist_boarder),(height/2-dist_boarder)*-1, 0])
         cylinder(h= height+1, r = screw_hole, center = true, $fn=100);

   txtsize = 20;
   
   color([1,0,0]) translate([7,45,-1]) rotate([0,180,0]) linear_extrude(2)
            text("N", font="Media Blackout:Regular", size = txtsize, spacing=1.2);
            
   color([1,0,0]) translate([7,20,-1]) rotate([0,180,0]) linear_extrude(2)
            text("E", font="Media Blackout:Regular", size = txtsize, spacing=1.2);

   color([1,0,0]) translate([7,-5,-1]) rotate([0,180,0]) linear_extrude(2)
            text("E", font="Media Blackout:Regular", size = txtsize, spacing=1.2);
            
   color([1,0,0]) translate([7,-30,-1]) rotate([0,180,0]) linear_extrude(2)
            text("D", font="Media Blackout:Regular", size = txtsize, spacing=1.2);
     
   color([1,0,0]) translate([7,-55,-1]) rotate([0,180,0]) linear_extrude(2)
            text("Y", font="Media Blackout:Regular", size = txtsize, spacing=1.2);
}

mount_inner_diameter = 1.9;
difference(){
   x1 = 27.5;
   y1 = 50;
   color("blue") translate([x1,y1, 2 + 0]) 
      cylinder(h = 5, d = mount_inner_diameter + 3);
   
   color("blue") translate([x1, y1, 2 + 0])
      cylinder(h = 5, d = mount_inner_diameter);
   
}

x3 = 27.5;
y3 = 15;
color("blue") translate([x3,y3, 2 + 0]) 
   cylinder(h = 5, d = mount_inner_diameter + 3);

x4 = -27.5;
y4 = 15;
color("blue") translate([x4,y4, 2 + 0]) 
   cylinder(h = 5, d = mount_inner_diameter + 3);

difference(){
   x2 = -27.5;
   y2 = 50;
   color("blue") translate([x2, y2, 2 + 0])
      cylinder(h = 5, d = mount_inner_diameter+3);
   
   color("blue") translate([x2, y2, 2 + 0])
      cylinder(h = 5, d = mount_inner_diameter);
}


