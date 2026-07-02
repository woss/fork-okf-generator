// Package strings provides additional string manipulation helpers.
package strings

import (
	"strings"
	"unicode"
)

// SnakeCase converts a CamelCase string to snake_case.
func SnakeCase(s string) string {
	var result strings.Builder
	for i, r := range s {
		if unicode.IsUpper(r) {
			if i > 0 {
				result.WriteRune('_')
			}
			result.WriteRune(unicode.ToLower(r))
		} else {
			result.WriteRune(r)
		}
	}
	return result.String()
}

// Truncate shortens a string to maxLen characters, appending "..." if truncated.
func Truncate(s string, maxLen int) string {
	if len(s) <= maxLen {
		return s
	}
	return s[:maxLen] + "..."
}

// Reverse returns a reversed copy of the input string.
func Reverse(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

// WordCount returns a map of word frequencies in the input string.
func WordCount(s string) map[string]int {
	counts := make(map[string]int)
	for _, word := range strings.Fields(s) {
		cleaned := strings.Trim(strings.ToLower(word), ".,!?;:\"'")
		if cleaned != "" {
			counts[cleaned]++
		}
	}
	return counts
}
