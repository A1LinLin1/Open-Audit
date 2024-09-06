import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class DangerousCodeExamples {

    public static void main(String[] args) throws IOException {
        String code = "Runtime.getRuntime().exec('ls -la');"; // 示例代码

        List<String> dangerousPatterns = new ArrayList<>();
        // 危险的种类
        dangerousPatterns.add("(Runtime)\\.(exec|getRuntime)\\.(exec)");
        dangerousPatterns.add("(ProcessBuilder|ProcessImpl)\\.(start)");
        dangerousPatterns.add("(UNIXProcess)\\.(forkAndExec)");
        dangerousPatterns.add("(Runtime)\\.(getRuntime()|load).(load)");
        dangerousPatterns.add("defineClass");
        dangerousPatterns.add("getOutputProperties");
        dangerousPatterns.add("createQuery");
        dangerousPatterns.add("executeQuery");
        dangerousPatterns.add("createNativeQuery");
        dangerousPatterns.add("doQuery");
        dangerousPatterns.add("preparedStatement.execute");
        dangerousPatterns.add("(URL|url)\\.(openConnection)");
        dangerousPatterns.add("(ImageIO)\\.(read)");
        dangerousPatterns.add("(JSON)\\.(parseObject|parse)");
        dangerousPatterns.add("(ObjectMapper)\\.(readValue)");
        dangerousPatterns.add("readObject");

        // 检查代码中是否包含危险的种类
        for (String patternStr : dangerousPatterns) {
            Pattern pattern = Pattern.compile(patternStr);
            Matcher matcher = pattern.matcher(code);
            while (matcher.find()) {
                System.out.println("Found potential vulnerability: " + matcher.group());
            }
        }
    }
}
