$fn=50;

// measurements for the base plate
width = 145;
height = 156;
thickness = 4;

difference(){
   // BASE PLATE
   translate([0,0,0])
   cube([width, height, thickness], center=true);

   // SCREW HOLES
   screw_hole = 3.5/2;
   dist_boarder = 6.5;

   color([1,0,0])
      translate([(145/2-dist_boarder),(145/2-dist_boarder + 4), 0])
         cylinder(h= height+1, r = screw_hole, center = true, $fn=100);

   color([1,0,0])
      translate([(145/2-dist_boarder)*-1,(145/2-dist_boarder+4), 0])
         cylinder(h= height+1, r = screw_hole, center = true, $fn=100);

   color([1,0,0])
      translate([(145/2-dist_boarder)*-1,(145/2-dist_boarder)*-1-4, 0])
         cylinder(h= height+1, r = screw_hole, center = true, $fn=100);

   color([1,0,0])
      translate([(145/2-dist_boarder),(145/2-dist_boarder)*-1-4, 0])
         cylinder(h= height+1, r = screw_hole, center = true, $fn=100);


   // BUTTONS
   button_hole = 16.5; // diameter
   x_offset = 52;
   y_offset = x_offset;

   // right
   color([1,0,0])
      translate([x_offset,0,0])
         cylinder(h = height+1, r = button_hole/2, center = true);

   // top
   color([1,0,0])
      translate([0,y_offset,0])
         cylinder(h = height+1, r = button_hole/2, center = true);

   // left
   color([1,0,0])
      translate([-x_offset,0,0])
         cylinder(h = height+1, r = button_hole/2, center = true);

   // bottom
   color([1,0,0])
      translate([0,-y_offset,0])
         cylinder(h = height+1, r = button_hole/2, center = true);
         
   // TEXT
  group(){
      color([1,0,0]) translate([63,-65,0]) rotate([0,180,0]) linear_extrude(2)
         text("AMAZE.......", font="Media Blackout:Regular", size = 15, spacing=1.2);
      color([1,0,0]) translate([-17.5,-65,0]) rotate([0,180,0]) linear_extrude(2)
         text("ing", font="Media Blackout", size = 15, spacing=1.2);
   }



   // LED MATRIX
   // WS2812 / WS2812b Led Matrix Diffuser by malebuffy

   PCB_HEIGHT = 66; // Size of PCB in mm
   PCB_WIDTH = 66; // Size of PCB in mm
   NUMBER_LEDS_HORIZONTAL=8; // Number of Leds in a row
   NUMBER_LEDS_VERTICAL=8;   // Number of Leds in a column
   DIFFUSER_HEIGHT = 2; // Height of diffuser
   LED_SIZE = 5; // Size of leds in mm
   DISTANCE_BETWEEN_LEDS=3.12; // Distance between leds in mm
   WALL_THINKESS=1; // Thinkess of walls
   PCB_BORDER = 0.4;  // PCB Outer Boarder in mm

   buffer=DISTANCE_BETWEEN_LEDS-WALL_THINKESS;
   translate([0,0,1])
         cube([67, 67, 3.5], center = true);
   group() {
      
      for ( i = [0:NUMBER_LEDS_HORIZONTAL-1] ) {
         translate([PCB_BORDER-32.5,(LED_SIZE+DISTANCE_BETWEEN_LEDS)*i-42.5+10,-1])

         for ( j = [0:NUMBER_LEDS_VERTICAL-1] ) {
            translate([(LED_SIZE+DISTANCE_BETWEEN_LEDS)*j,PCB_BORDER,-1])
            cube([LED_SIZE+buffer,LED_SIZE+buffer,DIFFUSER_HEIGHT+5]);    
         }
      }
   }
  
}



// TODO: neu aufhängung machen (durchmesser innen und aussen anpassen)
//positionierung anders machen wegen kabel für ledmatrix
mount_inner_diameter = 1.8;
difference(){
   color("blue") translate([17, 36, 2 + 0]) 
      cylinder(h = 8.5, d = mount_inner_diameter + 2.5);
   
   color("blue") translate([17, 36, 2 + 0])
      cylinder(h = 8.5, d = mount_inner_diameter);
   
}

difference(){
   color("blue") translate([17+11.3, 36, 2 + 0])
      cylinder(h = 8.5, d = mount_inner_diameter+2.5);
   
   color("blue") translate([17+11.3, 36, 2 + 0])
      cylinder(h = 8.5, d = mount_inner_diameter);
}




