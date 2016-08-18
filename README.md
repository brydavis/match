# Match

Package for matching / linking health records based on common best practices and established algorithms.

### Sketch (Doesn't Work)

```go
package main 

import (
  "fmt"
  ...
  
  "github.com/brydavis/match"
)

func main() {
  fmt.Println(match.String("Bryan", "Brien")) // True
  fmt.Println(match.String("ashcraft", "ashcroft")) // True
  ...
}
```
