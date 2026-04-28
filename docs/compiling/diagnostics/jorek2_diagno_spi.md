---
title: "Jorek2 Diagno Spi"
nav_order: 24
render_with_liquid: false
parent: "General"
---

The jorek2_diagno_spi diagnostics extracts some useful data from a JOREK restart file, including the SPI fragments position and radius at the time of the restart file.

The fragment positions are written to a file called `fragments_position.dat`. This file can be read in Paraview and plotted with a "Table To Points" filter as described in more detail below.

To load the text file: untick "Have headers", put a white space in the "Field Delimiter Characters" field, tick "Merge Consecutive Delimiters", and click "Apply".

To plot a point for each fragment: use a "Table To Points" filter. Select "Field 1" for the X Column and "Field 2" for the Y Column, tick "2D Points" and click "Apply".

Optionally, instead of a point you can also plot a circle whose radius depends on the fragment radius. To do this, in the "Table To Points" filter. Select "Field 1" for the X Column, "Field 2" for the Y Column, and "Field 4" for the Z Column. DO NOT tick "2D Points", and click "Apply". Then, to convert the points into circles, use in sequence a "Programmable Filter" with this script:

    import math
    fact = 5. # radius multiplication factor
    nv = 36 # number of vertices of the polygon around each shard
    pdi = self.GetPolyDataInput()
    pdo =  self.GetPolyDataOutput()
    numShards= pdi.GetNumberOfPoints() # number of shards
    # first we create all the points needed
    pts = vtk.vtkPoints()
    for i in range(0, numShards):
        coord = pdi.GetPoint(i)
        R, Z, radius = coord[:3]
        radius = fact*radius
        for j in range(0,nv+1):
            angle=j/nv*2.*math.pi
            pts.InsertNextPoint(R+radius*cos(angle),Z+radius*sin(angle),0)
    pdo.SetPoints(pts)
    # then we connect the points related to each shard
    pdo.Allocate()
    for i in range(0, numShards):
        pdo.InsertNextCell(3, nv+1, range<sup>[nv+1)*i,(nv+1)*(i+1]</sup>)
