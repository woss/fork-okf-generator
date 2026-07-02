package com.okfgen.java.model;

import java.time.LocalDateTime;
import java.util.Objects;

/**
 * Represents a user entity in the system.
 */
public class User {

    private final String id;
    private String email;
    private String displayName;
    private boolean active;
    private final LocalDateTime createdAt;

    /**
     * Constructs a new User with the given fields.
     *
     * @param id          unique identifier
     * @param email       email address
     * @param displayName optional display name
     */
    public User(String id, String email, String displayName) {
        this.id = id;
        this.email = email;
        this.displayName = displayName;
        this.active = true;
        this.createdAt = LocalDateTime.now();
    }

    /**
     * Constructs a minimal User with just an ID and email.
     *
     * @param id    unique identifier
     * @param email email address
     */
    public User(String id, String email) {
        this(id, email, null);
    }

    public String getId() {
        return id;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getDisplayName() {
        return displayName;
    }

    public void setDisplayName(String displayName) {
        this.displayName = displayName;
    }

    public boolean isActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof User user)) return false;
        return Objects.equals(id, user.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "User{" + "id='" + id + '\'' + ", email='" + email + '\'' + '}';
    }
}
