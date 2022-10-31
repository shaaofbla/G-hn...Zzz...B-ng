width = 60;
height = 156;
thickness = 4;

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


    // BUTTON HOLE
    button_hole = 28.3;
    cylinder(r=button_hole/2, h=10, center=true);   
}