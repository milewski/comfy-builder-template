use comfy_builder_core::prelude::*;

#[derive(NodeInput)]
pub struct Input {
    left: usize,
    right: usize,
}

#[derive(NodeOutput)]
pub struct Output {
    sum: usize,
}

#[node]
pub struct Sum;

impl<'a> Node<'a> for Sum {
    type In = Input;
    type Out = Output;

    const CATEGORY: &'static str = "MyNode / Math";

    const DESCRIPTION: &'static str = r#"
        Sums the left input with the right input.
    "#;

    fn execute(&self, input: Self::In) -> NodeResult<'a, Self> {
        Ok(Output {
            sum: input.left + input.right
        })
    }
}

boostrap!();
