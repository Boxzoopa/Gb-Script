// reflection.go
package helpers

import (
	"reflect"
	"fmt"
)

func ExpectType[T any](r any) T {
	expectedtype := reflect.TypeOf((*T)(nil)).Elem()
	recievedtype := reflect.TypeOf(r)
	if expectedtype == recievedtype {
		return r.(T)
	}
	panic(fmt.Sprintf("Expected %T but recieved %T instead.", expectedtype, recievedtype))
}