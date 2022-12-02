use std::fs::File;
use std::io::{
    BufRead,
    BufReader,
    self,
};
use std::path::Path;



// The output is wrapped in a Result to allow matching on errors
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<BufReader<File>>>
    where
        P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(BufReader::new(file).lines())
}



fn parse(hands_line: String) -> (char, char) {
    let hands: Vec<char> = hands_line
        .chars()
        .into_iter()
        .filter(|&c| c.is_alphabetic())
        .collect();
    let other = hands[0];
    let you   = hands[1];
    (other, you)
}



fn calculate_score(other: char, you: char) -> u32 {
    match (other, you) {
        // Rock
        ('A', 'X') => 3 + 1,   // Rock
        ('A', 'Y') => 6 + 2,   // Paper
        ('A', 'Z') => 0 + 3,   // Scissors
        // Paper
        ('B', 'X') => 0 + 1,   // Rock
        ('B', 'Y') => 3 + 2,   // Paper
        ('B', 'Z') => 6 + 3,   // Scissors
        // Scissors
        ('C', 'X') => 6 + 1,   // Rock
        ('C', 'Y') => 0 + 2,   // Paper
        ('C', 'Z') => 3 + 3,   // Scissors
        (_, _) => 0,
    }
}



/// What would your total score be if everything goes exactly according to your strategy guide?
fn part1() -> u32 {
    let mut score: u32 = 0;
    let data = read_lines("data").unwrap();
    for line in data {
        if let Ok(hands_line) = line {
            let hands: Vec<char> = hands_line
                .chars()
                .into_iter()
                .filter(|&c| c.is_alphabetic())
                .collect();
            //println!("{:?}", hands);
            let other = hands[0];
            let you = hands[1];
            //println!("{} {}", other, you);
            score += calculate_score(other, you);
        }
    }
    return score;
}



fn part1_it() -> u32 {
    read_lines("data")
        .unwrap()
        .map(Result::unwrap)
        .map(|hands_line| parse(hands_line))
        .map(|(other, you)| calculate_score(other, you))
        .sum()
}



/// Return the hand you should be playing in order to draw, lose or win.
fn whatShouldYouPlay(other: char, you: char) -> char {
    match (you, other) {
        // Lose
        ('X', 'A') => 'Z',   // Rock
        ('X', 'B') => 'X',   // Paper
        ('X', 'C') => 'Y',   // Scissors
        // Draw
        ('Y', 'A') => 'X',   // Rock
        ('Y', 'B') => 'Y',   // Paper
        ('Y', 'C') => 'Z',   // Scissors
        // Win
        ('Z', 'A') => 'Y',   // Rock
        ('Z', 'B') => 'Z',   // Paper
        ('Z', 'C') => 'X',   // Scissors
        (_, _) => 'I',
    }
}



/// What would your total score be if everything goes exactly according to your strategy guide?
fn part2() -> u32 {
    let mut score: u32 = 0;
    let data = read_lines("data").unwrap();
    for line in data {
        if let Ok(hands_line) = line {
            let hands: Vec<char> = hands_line
                .chars()
                .into_iter()
                .filter(|&c| c.is_alphabetic())
                .collect();
            //println!("{:?}", hands);
            let other = hands[0];
            let you = whatShouldYouPlay(other, hands[1]);
            //println!("{} {}", other, you);
            score += calculate_score(other, you);
        }
    }
    return score;
}



/// What would your total score be if everything goes exactly according to your strategy guide?
fn part2_it() -> u32 {
    read_lines("data")
        .unwrap()
        .map(Result::unwrap)
        .map(|hands_line| parse(hands_line))
        .map(|(other, you)| (other, whatShouldYouPlay(other, you)))
        .map(|(other, you)| calculate_score(other, you))
        .sum()
}



fn main() {
    {
        let answer = part1_it();
        println!("Part1: {}", answer);
        assert!(answer == 17189);
    }

    {
        let answer = part2_it();
        println!("Part2: {}", answer);
        assert!(answer == 13490);
    }
}
