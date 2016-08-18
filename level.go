package main

import "fmt"

func main() {
	s1 := "rosettacode"
	s2 := "raisethysword"

	fmt.Println(ld1("kitten", "sitting") == ld2("kitten", "sitting"))
	fmt.Println(ld1(s1, s2) == ld2(s1, s2))

}

func ld1(s, t string) int {
	d := make([][]int, len(s)+1)
	for i := range d {
		d[i] = make([]int, len(t)+1)
	}
	for i := range d {
		d[i][0] = i
	}
	for j := range d[0] {
		d[0][j] = j
	}
	for j := 1; j <= len(t); j++ {
		for i := 1; i <= len(s); i++ {
			if s[i-1] == t[j-1] {
				d[i][j] = d[i-1][j-1]
			} else {
				min := d[i-1][j]
				if d[i][j-1] < min {
					min = d[i][j-1]
				}
				if d[i-1][j-1] < min {
					min = d[i-1][j-1]
				}
				d[i][j] = min + 1
			}
		}

	}
	return d[len(s)][len(t)]
}

func ld2(s, t string) int {
	if s == "" {
		return len(t)
	}
	if t == "" {
		return len(s)
	}
	if s[0] == t[0] {
		return ld2(s[1:], t[1:])
	}
	a := ld2(s[1:], t[1:])
	b := ld2(s, t[1:])
	c := ld2(s[1:], t)
	if a > b {
		a = b
	}
	if a > c {
		a = c
	}
	return a + 1
}
