package docsgenerator;

import static java.nio.file.StandardOpenOption.*;

import binder.command.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

public final class Main {

    public static void main(String[] args) {
        Command.commandsPerNamespace.forEach((namespace, commands) -> {
            var header = "<h1>" + namespace + "</h1><p>" + Descriptions.getNamespaceDescription(namespace) + "</p><hr>";
            var functions = commands.stream()
                                    .sorted(Comparator.comparing(k -> k.function))
                                    .map(k -> "<h2>" + k.function + '(' + k.editorSignature + ")</h2>" + getCommandDescription(k))
                                    .collect(Collectors.joining("<hr>"));
            try {
                Files.writeString(Path.of("../docs/pages/commands/" + namespace + ".html"), header + functions, CREATE, TRUNCATE_EXISTING);
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
    }

    private static String getCommandDescription(Command command) {
        return "<h4>Description:</h4>" +
               "<p>" + Descriptions.getCommandDescription(command) + "</p>" +
               "<h4>Example:</h4>" +
               "<p class = \"code-example\">" + getCommandExample(command) + "</p>";
    }

    private static String getCommandExample(Command command) {
        var parameters = switch(command) {
            case MOUSE_CLICK                        -> new String[] { createEnumParam("button", "right") };
            case MOUSE_MOVE_ABSOLUTE                -> new String[] { createIntegerParam("x", 50), createIntegerParam("y", 50) };
            case MOUSE_MOVE_RELATIVE                -> new String[] { createIntegerParam("x", 50), createIntegerParam("y", 50) };
            case KEYBOARD_TYPE                      -> new String[] { createStringParam("text", "hi team") };
            case KEYBOARD_HOLD                      -> new String[] { createEnumParam("key", "SHIFT") };
            case KEYBOARD_RELEASE                   -> new String[] { createEnumParam("key", "SHIFT") };
            case COMMON_COPY_SELECTION_TO_CLIPBOARD -> new String[] {};
            case COMMON_COPY_TEXT_TO_CLIPBOARD      -> new String[] { createStringParam("text", "epic text") };
            case COMMON_EXEC                        -> new String[] { createStringParam("command", "explorer https://google.com") };
            case COMMON_WAIT_MS                     -> new String[] { createIntegerParam("time", 250) };

            case PPRO_ADJUST_GAIN                   -> new String[] { createIntegerParam("level", 5) };

            case OBS_RESTART_MEDIA_SOURCE           -> new String[] { createStringParam("source", "hidden-porn") };
            case OBS_SET_MEDIA_SOURCE_PAUSE         -> new String[] { createStringParam("source", "epic-frag"), createBooleanParam("paused", true) };
            case OBS_SET_SOURCE_MUTED               -> new String[] { createStringParam("source", "duc-duc"), createBooleanParam("muted", false) };
            case OBS_START_RECORDING                -> new String[] {};
            case OBS_STOP_MEDIA_SOURCE              -> new String[] { createStringParam("source", "background-music") };
            case OBS_TOGGLE_MEDIA_SOURCE_PAUSE      -> new String[] { createStringParam("source", "intro") };
            case OBS_TOGGLE_SOURCE_MUTED            -> new String[] { createStringParam("source", "outro-music") };

            case CG_CREATECLIP                      -> new String[] { createStringParam("channel", "wearethevr") };
            case CG_WRITELINE                       -> new String[] { createStringParam("text", "Hello World") };

            case TWITCH_CREATE_CLIP                 -> new String[] { createStringParam("channel", "shroud") };
        };

        return command.namespace + '.' + command.function + '(' + String.join(", ", parameters) + ')';
    }

    private static String createIntegerParam(String name, int value) {
        return name + " = <span class = \"integer-param\">" + value + "</span>";
    }

    private static String createEnumParam(String name, String value) {
        return name + " = <span class = \"enum-param\">" + value + "</span>";
    }

    private static String createStringParam(String name, String value) {
        return name + " = <span class = \"string-param\">'" + value + "'</span>";
    }

    private static String createBooleanParam(String name, boolean value) {
        return name + " = <span class = \"boolean-param\">" + value + "</span>";
    }
}