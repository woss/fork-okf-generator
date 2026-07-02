package com.okfgen.java.util;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

/**
 * Utility methods for string manipulation.
 */
public final class StringUtils {

    private static final Pattern EMAIL_PATTERN =
            Pattern.compile("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$");

    private StringUtils() {
        throw new UnsupportedOperationException("Utility class cannot be instantiated");
    }

    /**
     * Checks whether the given string is a valid email address.
     *
     * @param email the string to validate
     * @return true if the string matches basic email format
     */
    public static boolean isValidEmail(String email) {
        return email != null && EMAIL_PATTERN.matcher(email).matches();
    }

    /**
     * Truncates a string to the specified maximum length.
     *
     * @param text    the input string
     * @param maxLen  maximum allowed length
     * @return truncated string with "..." appended if shortened
     */
    public static String truncate(String text, int maxLen) {
        if (text == null || text.length() <= maxLen) {
            return text;
        }
        return text.substring(0, Math.max(0, maxLen - 3)) + "...";
    }

    /**
     * Converts a CamelCase string to snake_case.
     *
     * @param camel the CamelCase input
     * @return snake_case string
     */
    public static String toSnakeCase(String camel) {
        if (camel == null || camel.isEmpty()) {
            return camel;
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < camel.length(); i++) {
            char c = camel.charAt(i);
            if (Character.isUpperCase(c)) {
                if (i > 0) {
                    sb.append('_');
                }
                sb.append(Character.toLowerCase(c));
            } else {
                sb.append(c);
            }
        }
        return sb.toString();
    }

    /**
     * Splits a string into chunks of the given size.
     *
     * @param text  the input string
     * @param size  chunk size in characters
     * @return list of string chunks
     */
    public static List<String> chunk(String text, int size) {
        List<String> chunks = new ArrayList<>();
        if (text == null || size <= 0) {
            return chunks;
        }
        for (int i = 0; i < text.length(); i += size) {
            chunks.add(text.substring(i, Math.min(i + size, text.length())));
        }
        return chunks;
    }
}
