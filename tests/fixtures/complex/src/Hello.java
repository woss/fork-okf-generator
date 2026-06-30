import java.util.List;
import java.util.ArrayList;

/**
 * Greeting service with user management.
 */
public class Hello {

    private String greeting;
    private List<String> names;

    /** Creates a new Hello instance. */
    public Hello(String greeting) {
        this.greeting = greeting;
        this.names = new ArrayList<>();
    }

    /**
     * Adds a name to the greeting list.
     * @param name the name to add
     */
    public void addName(String name) {
        names.add(name);
    }

    /**
     * Returns a greeting for all added names.
     * @return combined greeting string
     */
    public String greetAll() {
        StringBuilder sb = new StringBuilder();
        for (String name : names) {
            sb.append(greeting).append(", ").append(name).append("!\n");
        }
        return sb.toString();
    }
}
