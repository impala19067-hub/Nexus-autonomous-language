// 01_basics.sp - Sapphire Language Language Syntax & Basics

fn add(a, b) -> int {
    return a + b;
}

fn calculate_discount(price, rate) {
    let discount = price * (rate / 100);
    return price - discount;
}

fn main() {
    print("âœ¨ Welcome to Sapphire Language v1.0");

    let name = "Developer";
    let score = 98.5;
    let languages = ["Python", "Rust", "Go", "Sapphire"];

    print("User: {name}, Score: {score}");

    print("Supported Languages:");
    for lang in languages {
        print(" -> {lang}");
    }

    let final_price = calculate_discount(200, 15);
    print("Final Price after discount: {final_price}");
}

main();

