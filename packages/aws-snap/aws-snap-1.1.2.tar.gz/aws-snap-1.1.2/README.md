# aws-snap   
   
Create snapshots of AWS EC2 instance volumes.   
   
## installation   
   
`pip install aws-snap`   
   
this should install the CLI tool `aws-snap` and `snapit`   
_the two are interchangable_   
   
## usage   
   
`snapit -h` # show help and exit   
   
`snapit i-0d2bd932gf7de4c95` # create snapshot of instance with ID i-0d2bd932gf7de4c95   
   
`snapit i-0d2bd932gf7de4c95 i-67dfg98s0ijj6y2j0` # snapshots of multiple instances   
   
`snapit i-0d2bd932gf7de4c95 -r us-west-1` # specify a region other than the one set in your profile   
   
`snapit i-0d2bd932gf7de4c95 -s` # stop the instance before snapping   
   
